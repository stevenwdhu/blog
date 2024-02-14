pkill -e gunicorn
sleep 0.5
echo "\ngunicorn starting..."
gunicorn -c "$(dirname "$(readlink -f "$0")")"/gunicorn.conf.py blog.wsgi:application
sleep 0.5
pgrep -l gunicorn