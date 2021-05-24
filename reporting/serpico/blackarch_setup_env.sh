#!/usr/bin/env bash
# blackarch_setup_env.sh

cd /opt

echo "Installing tools via yay"
yay -S python-pip openvpn go brutespray nmap libxslt sslscan tmux parallel ike-scan \
  trufflehog seclists aquatone corscanner gospider dalfox subfinder httpx dnsx nuclei \
  sslyze naabu proxify

echo "Fetching custom NSE"
sudo git clone https://github.com/r3naissance/nse && \
  sudo cp nse/*.nse /usr/share/nmap/scripts/ && \
  sudo nmap --script-updatedb

echo "Fetch nmap bootstrap"
sudo git clone https://github.com/honze-net/nmap-bootstrap-xsl

echo "updating nuclei templates"
nuclei --update-templates

echo "done"
