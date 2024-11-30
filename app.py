from flask import Flask, jsonify, render_template_string
import os
import platform
import socket
import datetime
import psutil

app = Flask(__name__)

# HTML template with styling
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Docker Flask Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .info-card {
            background-color: #f8f9fa;
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .info-title {
            color: #34495e;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #7f8c8d;
            font-size: 0.9em;
        }
        .status-ok {
            color: #27ae60;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐳 Docker Flask Demo</h1>
        
        <div class="info-card">
            <div class="info-title">System Information</div>
            <p>Hostname: {{ hostname }}</p>
            <p>Platform: {{ platform }}</p>
            <p>IP Address: {{ ip_address }}</p>
        </div>
        
        <div class="info-card">
            <div class="info-title">Container Stats</div>
            <p>CPU Usage: {{ cpu_usage }}%</p>
            <p>Memory Usage: {{ memory_usage }}MB</p>
            <p>Uptime: {{ uptime }}</p>
        </div>
        
        <div class="info-card">
            <div class="info-title">Environment</div>
            <p>Python Version: {{ python_version }}</p>
            <p>Flask Version: {{ flask_version }}</p>
            <p>Status: <span class="status-ok">✓ Running</span></p>
        </div>

        <div class="footer">
            <p>Created by Md Toriqul Islam | <a href="https://github.com/TheToriqul">GitHub</a></p>
        </div>
    </div>
</body>
</html>
'''

def get_container_stats():
    """Get container resource usage stats"""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.Process(os.getpid()).memory_info()
    memory_usage = round(memory.rss / 1024 / 1024, 2)  # Convert to MB
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    return cpu_usage, memory_usage, str(uptime).split('.')[0]

@app.route('/')
def home():
    """Home page with system information"""
    cpu_usage, memory_usage, uptime = get_container_stats()
    
    return render_template_string(HTML_TEMPLATE,
        hostname=socket.gethostname(),
        platform=platform.platform(),
        ip_address=socket.gethostbyname(socket.gethostname()),
        cpu_usage=cpu_usage,
        memory_usage=memory_usage,
        uptime=uptime,
        python_version=platform.python_version(),
        flask_version=Flask.__version__
    )

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/info')
def info():
    """Container information endpoint"""
    cpu_usage, memory_usage, uptime = get_container_stats()
    
    return jsonify({
        'container': {
            'hostname': socket.gethostname(),
            'platform': platform.platform(),
            'ip_address': socket.gethostbyname(socket.gethostname())
        },
        'resources': {
            'cpu_usage': f"{cpu_usage}%",
            'memory_usage': f"{memory_usage}MB",
            'uptime': str(uptime)
        },
        'versions': {
            'python': platform.python_version(),
            'flask': Flask.__version__
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)