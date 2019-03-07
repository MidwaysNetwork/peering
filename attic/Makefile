IX=sfinx pouix freeix geix panap

check:
	@echo = Making check...
	@nsgmls -s -wxml /usr/share/sgml/declaration/xml.dcl peers.xml
	@echo = check done.

peers.xml: check

all: install zebra-moniteur.conf ripe-send

install: as20766.txt
	@echo = Making install...
	(cd /var/www-gitoyen/routing; make -W peers.wml)
	for ix in ${IX}; do\
		./peers2bgpConfig.pl peers.xml $$ix > peers-$$ix-bgpd.conf;\
		./peers2bind.pl peers.xml $$ix > db.$$ix-peers.gitoyen.net;\
		cp db.$$ix-peers.gitoyen.net /etc/bind/;\
		rndc reload $$ix-peers.gitoyen.net;\
        done
	@echo = Copying peers.xml to w3

zebra-moniteur.conf: peers.xml peers2fdnMoniteurConfig.pl
	@echo = Making zebra-moniteur.conf...
	./peers2fdnMoniteurConfig.pl peers.xml > zebra-moniteur.conf
	@cp zebra-moniteur.conf /var/www/gitoyen/
	@echo = zebra-moniteur.conf done.

as20766.txt: as20766.epy peers.xml
	@echo = Making as20766.txt...
	./peers2fdnMoniteurConfig.pl peers.xml > zebra-moniteur.conf
	./myepython < as20766.epy > as20766.txt
	@echo = as20766.txt done.

ripe: as20766.txt.asc

as20766.txt.asc: as20766.txt
	@echo = Making as20766.txt.asc...
	gpg --clearsign --armor --yes --default-key gitoyen $<
#	  --keyring ~bortzmeyer/.gnupg/pubring.gpg \
#	  --secret-keyring ~bortzmeyer/.gnupg/secring.gpg $<
	@echo = Making as20766.txt.asc...

ripe-send: as20766.txt.asc
	@echo = Making ripe-send...
	mutt -s "MODIFY KEYWORDS:DIFF" -e 'my_hdr X-NCC-Regid: fr.gitoyen' \
		auto-dbm@ripe.net < $<
	@echo = ripe-send done.

peers.dvi: peers.tex
	latex peers.tex

peers.tex: peers.xml to-latex.xslt
	xsltproc -o $@ to-latex.xslt peers.xml

peers.db: peers.xml to-docbook.xslt
	xsltproc -o $@ to-docbook.xslt peers.xml

clean:
	rm -f *.dvi *.tmp *.aux *.log as20766.txt.asc as20766.txt peers.tex peers.db 
	rm -f peers*-bgpd.conf db.*-peers.gitoyen.net zebra-moniteur.conf *~

bgp-show:
	@[ -n "${IX}" ] && echo IX=${IX}
	@[ -n "${ASN}" ] && echo ASN=${ASN}
	@./peers2bgpConfig.pl peers.xml ${IX} ${ASN}

