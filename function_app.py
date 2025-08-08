import json
import azure.functions as func
import logging

app = func.FunctionApp()

# @app.queue_trigger(arg_name="azqueue", queue_name="getsummary",
#                                connection="aegntfuncstore_STORAGE") 
# def getsummary(azqueue: func.QueueMessage):
#     logging.info('Python Queue trigger processed a message: %s',
#                 azqueue.get_body().decode('utf-8'))

@app.queue_trigger(arg_name="msg", queue_name="azure-function-foo-input", connection="STORAGE_CONNECTION")
@app.queue_output(arg_name="outputQueue", queue_name="azure-function-foo-output", connection="STORAGE_CONNECTION")  

def queue_trigger(msg: func.QueueMessage, outputQueue: func.Out[str]):
    try:
        messagepayload = json.loads(msg.get_body().decode("utf-8"))
        logging.info(f'The function receives the following message: {json.dumps(messagepayload)}')
        location = messagepayload["location"]
        weather_result = f"Weather is {len(location)} degrees and sunny in {location}"
        response_message = {
            "Value": weather_result,
            "CorrelationId": messagepayload["CorrelationId"]
        }

        logging.info(f'The function returns the following message through the {outputQueue} queue: {json.dumps(response_message)}')

        outputQueue.set(json.dumps(response_message))

    except Exception as e:
        logging.error(f"Error processing message: {e}")
