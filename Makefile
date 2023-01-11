mode?=
ifdef mode
	mode:=${mode}
endif
export MODE=${mode}

export POLYGONBOT_PORT=5004
export SLACKBOT_PORT=5003
export MQTT_PORT=1884

USERNAME?=$(shell whoami)
USER_ID?=$(shell id -u)
GROUP_ID?=$(shell id -g)

build:
	docker-compose -f docker-compose.yml -f docker-compose.${mode}.yml build --build-arg USERNAME=${USERNAME} --build-arg USER_ID=${USER_ID} --build-arg GROUP_ID=${GROUP_ID}

start:
	docker-compose -f docker-compose.yml -f docker-compose.${mode}.yml up -d

clean:
	docker-compose -f docker-compose.yml -f docker-compose.${mode}.yml down --remove-orphans
