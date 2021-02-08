.PHONY: build runlocal stoplocal
build:
	docker build -t thisisyourlife .

runlocal:
	docker run -d --rm --name thisisyourlife-local -p 80:80 thisisyourlife

stoplocal:
	docker container stop $$(docker ps | grep thisisyourlife | awk '{print $$1}') 

rerun: stoplocal build runlocal
