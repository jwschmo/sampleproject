from flask import Flask
from threading import Event
import signal
from TrendCalculations.TrendAlignment import TrendAlignment

from flask_kafka import FlaskKafka
app = Flask(__name__)

INTERRUPT_EVENT= Event()

bus = FlaskKafka(INTERRUPT_EVENT,
                 bootstrap_servers=",".join(["localhost:9092"]),
                 group_id="consumer-grp-id"
                 )

trendAlign = TrendAlignment()

def listen_stage_estimation():
    print(trendAlign.getStageEst(symbol="DIS"))
    signal.signal(signal.SIGTERM, bus.interrupted_process)
    signal.signal(signal.SIGINT, bus.interrupted_process)
    signal.signal(signal.SIGQUIT, bus.interrupted_process)
    signal.signal(signal.SIGHUP, bus.interrupted_process)

@bus.handle('test-topic')
def test_topic_handler(msg):
    print("consumed {} from test-topic".format(msg))

if __name__ == '__main__':
    bus.run()
    listen_stage_estimation()
    app.run(debut=True, port=5004)
