from .producer import KafkaLoggingProducer

# TODO 1 - Implement the KafkaLoggingMiddleware class
# TODO 2 - Create structure for vision-logs topic
# TODO 3 - Create integration with elastic search/kibana
# TODO 4 - Create a dashboard in kibana to visualize the logs

class KafkaLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.kafka_producer = KafkaLoggingProducer(servers=['kafka-server:9092'], topic='vision-logs')

    def __call__(self, request):
        response = self.get_response(request)
        self.log_request(request, response)
        return response

    def log_request(self, request, response):
        log_data = {
            'method': request.method,
            'path': request.get_full_path(),
            'status_code': response.status_code
        }
        self.kafka_producer.log(log_data)
