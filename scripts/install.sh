#!/bin/bash
#set -e

PROJECT_PATH="$(realpath "$(dirname "$0")/..")"
CONFIG_PATH="$PROJECT_PATH/scripts/config"

APT_WENUAPI_DEPS="nginx mysql-server libmysqlclient-dev python-dev"
APT_TASKS_DEPS="redis-server"
APT_COMMON_DEPS="virtualenv"

SYSTEMD_WENUAPI_SERVICE="wenuapi.service"
SYSTEMD_TASKS_NPROCS=2
SYSTEMD_TASKS_SERVICE="wenuapi-tasks@.service"
SYSTEMD_SERVICE_PATH="/etc/systemd/system"

SYSTEMD_SERVICE_PATH=/tmp
alias systemctl=true
alias apt-get=true
alias pip=true

APT_DEPS="$APT_COMMON_DEPS $APT_WENUAPI_DEPS $APT_TASKS_DEPS"
REQUIREMENTS="requirements-client.txt requirements-task_runner.txt requirements.txt"



satisfied(){
    local REQUIREMENT="$1"
    local FILE="$2"
    echo "$REQUIREMENT statisfied by $FILE, skipping $REQUIREMENT"
}

map(){
    for arg in "$@"; do
        printf "%s" "-r $arg"
    done
    echo
}

apt-get install $APT_DEPS

if [ -d "$PROJECT_PATH/.venv" ]; then
    satisfied "Virtual env" "$PROJECT_PATH/.venv"
else
    virtualenv "$PROJECT_PATH/.venv"
    . "$PROJECT_PATH/.venv/bin/activate"
    pip install $(map -r $REQUIREMENTS)
fi

if [ -f "$SYSTEMD_SERVICE_PATH/$SYSTEMD_TASKS_SERVICE" ]; then
    satisfied "Systemd tasks service" "$SYSTEMD_SERVICE_PATH/$SYSTEMD_TASKS_SERVICE"
else
    sed -r "s%@PROJECT_PATH@%$PROJECT_PATH%g" "$CONFIG_PATH/$SYSTEMD_TASKS_SERVICE" > "$SYSTEMD_SERVICE_PATH/$SYSTEMD_TASKS_SERVICE"
    systemctl daemon-reload
    for i in $(seq $SYSTEMD_TASKS_NPROCS); do
        systemctl enable $SYSTEMD_TASKS_SERVICE@$i
        systemctl start $SYSTEMD_TASKS_SERVICE@$i
    done
fi

if [ -f "$SYSTEMD_SERVICE_PATH/$SYSTEMD_WENUAPI_SERVICE" ]; then
    satisfied "Systemd wenuapi service" "$SYSTEMD_SERVICE_PATH/$SYSTEMD_WENUAPI_SERVICE"
else
    sed -r "s%@PROJECT_PATH@%$PROJECT_PATH%g" "$CONFIG_PATH/$SYSTEMD_WENUAPI_SERVICE" > "$SYSTEMD_SERVICE_PATH/$SYSTEMD_WENUAPI_SERVICE"
    systemctl daemon-reload
    systemctl enable $SYSTEMD_WENUAPI_SERVICE
    systemctl start $SYSTEMD_WENUAPI_SERVICE
fi

