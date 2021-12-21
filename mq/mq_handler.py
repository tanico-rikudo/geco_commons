
import pika
import uuid
class MqProvider(object):
    def __init__(self, mqserver_host, mqname, routing_key, logger):
        self.mqserver_host = mqserver_host
        self.mqname  = mqname
        self.routing_key = routing_key
        self.logger = logger

        
    def connect_mq(self):

        self.connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=self.mqserver_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.mqname)
        self.logger.info(f"[DONE] Connect MQ server. Host={self.mqserver_host}, Name={self.mqname}, Routing={self.routing_key}")
        
    def publish_mq(self, data, exchange='', routing_key=None,properties=None ):  
        exchange = '' if exchange is None else exchange
        routing_key = self.routing_key if routing_key is None else routing_key
        self.channel.basic_publish(exchange=exchange,
                                    routing_key=routing_key,
                                    properties= properties,
                                    body=data)
        self.logger.info(f"[DONE] Send data via MQ. Host={self.mqserver_host}, Name={self.mqname}, Routing={self.routing_key}")
        
    def close_mq(self):
        self.channel.basic_cancel() # declare no more send
        self.connection.close()
        self.logger.info(f"[DONE] Close MQ connecton. Host={self.mqserver_host}, Name={self.mqname}, Routing={self.routing_key}")
        
        
        
class RpcClient(object):

    def __init__(self, mqserver_host, routing_key, logger):
        self.mqserver_host = mqserver_host
        self.routing_key = routing_key
        
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.mqserver_host))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)
        
        self.logger.info(f"[STOP] RPC request client initilized. Host={mqserver_host}, Routing={routing_key}")

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, commannd_msg=None):
        commannd_msg = "" if commannd_msg is None else commannd_msg
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.logger(f"[REQUEST] Call RPC. ID={self.corr_id}, Command={commannd_msg}")
        self.channel.basic_publish(
            exchange='',
            routing_key=self.routing_key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(commannd_msg))
        while self.response is None:
            self.connection.process_data_events()
        return self.response
    
    
    def end_call(self):
        self.call("END")


        
    
