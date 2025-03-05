from metacognitive.stream.stream_provider.http_stream.http_stream import HTTPStream
from waitress import serve

http_stream = HTTPStream(port=7072)
app = http_stream.app

@app.route('/health', methods=['GET'])
def health_check():
    return '{"status":"ok"}', 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=7072, threads=1000)