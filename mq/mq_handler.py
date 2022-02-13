import pika
import uuid
import time

def load_mq_settings(general_config):
    use_mq = general_config.get("USE_MQ")
    if use_mq:
        mqserver_host = general_config.get("MQ_HOST")
        mqname = {
            "realtime": general_config.get("REALTIMEFEED_MQ_NAME"),
            "historical": general_config.get("HISTORICAL_MQ_NAME"),
        }
        routing_key = {
            "realtime": general_config.get("REALTIMEFEED_MQ_ROUTING"),
            "historical": general_config.get("HISTORICAL_MQ_ROUTING"),
        }
    else:
        mqserver_host = None
        mqname = {}
        routing_key = {}
    
    return {"mqserver_host":mqserver_host, "mqname":mqname, "routing_key":routing_key}


class MqProvider(object):
    def __init__(self, mqserver_host, mqname, routing_key, logger):
        self.mqserver_host = mqserver_host
        self.mqname = mqname
        self.routing_key = routing_key
        self.logger = logger

    def connect_mq(self):
        self.logger.info(
            f"[START] Connect MQ server... Host={self.mqserver_host}, Name={self.mqname}, Routing={self.routing_key}")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.mqserver_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.mqname)
        self.logger.info(
            f"[DONE] Connect MQ server. Host={self.mqserver_host}, Name={self.mqname}, Routing={self.routing_key}")

    def publish_mq(self, data, exchange='', routing_key=None, properties=None):
        exchange = '' if exchange is None else exchange
        routing_key = self.routing_key if routing_key is None else routing_key
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=routing_key,
                                   properties=properties,
                                   body=data)
        self.logger.info(
            f"[DONE] Send data via MQ. Host={self.mqserver_host}, Name={self.mqname}, Routing={self.routing_key}")

    def close_mq(self):
        try:
            self.channel.basic_cancel()  # declare no more send
            self.connection.close()
            self.logger.info(
                f"[DONE] Close MQ connecton. Host={self.mqserver_host}, Name={self.mqname}, Routing={self.routing_key}")
        except Exception as e:
            self.logger.warning("Fail to close mq safety")

class RpcClient(object):

    def __init__(self, mqserver_host, mqname, routing_key, logger):
        self.mqserver_host = mqserver_host
        self.mqname = mqname
        self.routing_key = routing_key
        self.logger = logger

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.mqserver_host))

        self.channel = self.connection.channel()

        # result = self.channel.queue_declare(queue=self.mqname, exclusive=True)
        result = self.channel.queue_declare(queue=self.mqname, exclusive=False)

        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.logger.info(f"[DONE] RPC request client initilized. Host={mqserver_host}, Routing={routing_key}")

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, commannd_msg=None):
        commannd_msg = "" if commannd_msg is None else commannd_msg
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.logger.info(f"[REQUEST] Call RPC. ID={self.corr_id}, Command={commannd_msg}, Roiting={self.routing_key}")
        self.channel.basic_publish(
            exchange='',
            routing_key=self.routing_key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(commannd_msg))
        #Note:  anxious....
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def end_call(self):
        self.call("END")
