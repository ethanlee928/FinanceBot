mode?=
ifdef mode
	mode:=${mode}
endif
export MODE=${mode}

build:
	docker-compose -f docker-compose.yml -f docker-compose.${mode}.yml build

start:
	docker-compose -f docker-compose.yml -f docker-compose.${mode}.yml up -d

clean:
	docker-compose -f docker-compose.yml -f docker-compose.${mode}.yml down --remove-orphans
