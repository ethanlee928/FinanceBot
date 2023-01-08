mode?=
ifdef mode
	mode:=${mode}
endif
export MODE=${mode}

export POLYGONBOT_PORT=5004
export SLACKBOT_PORT=5003
export MQTT_PORT=1884

build:
	docker-compose -f docker-compose.yml -f docker-compose.${mode}.yml build

start:
	docker-compose -f docker-compose.yml -f docker-compose.${mode}.yml up -d

clean:
	docker-compose -f docker-compose.yml -f docker-compose.${mode}.yml down --remove-orphans
