
import json
from jinja2 import Environment

env = Environment()

apps = json.load(open("apps.json"))

stream_template = '''
stream {
    {% for app in apps %}
    upstream {{ app.name }}-upstream {
        server {{ app.server }};
    }
    {% endfor %}

    map $ssl_preread_server_name $name {
        {% for app in apps %}{% for domain in app.domains %}{{ domain }} {{ app.name }}-upstream;{% endfor %}{% endfor %}
    }

    proxy_protocol on;

    server {
        listen      443;
        proxy_pass  $name;
        ssl_preread on;
    }
}
'''

with open('./stream.conf', 'w') as stream:
    stream.write(env.from_string(stream_template).render(apps=apps))


redirect_template = '''
{% for app in apps %}
{% for domain in app.domains %}
server {
    listen 80;
    server_name {{ domain }};
    return 301 https://{{ app.domain }}$request_uri;
}
{% endfor %}
{% endfor %}
'''

with open('./redirects.conf', 'w') as stream:
    stream.write(env.from_string(redirect_template).render(apps=apps))
