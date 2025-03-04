# from dotenv import load_dotenv
# import os

from metacognitive.stream.stream_provider.http_stream.http_stream import HTTPStream

http_stream = HTTPStream(port=7072)
app = http_stream.app
# load_dotenv()
# print(f"Redis configuration - Host: {os.getenv('REDIS_HOST', 'Not set')}, Port: {os.getenv('REDIS_PORT', 'Not set')}")

@app.route('/health', methods=['GET'])
def health_check():
    return '{"status":"ok"}', 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7072)