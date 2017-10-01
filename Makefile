crx:
	./extension/make_crx.sh ./extension/src/ ./extension/key.pem

xpi:
	./extension/make_xpi.sh

.PHONY: crx xpi
