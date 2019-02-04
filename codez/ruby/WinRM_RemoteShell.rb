# Notes: 
# https://github.com/WinRb/WinRM
# sudo gem install -r winrm
# sudo gem install -r openssl
# https://172.16.54.12/certsrv/ 
# used to create self-signed certs correctly --
# openssl req -out CSR.csr -new -newkey rsa:2048 -nodes -keyout privateKey.key
# upload CSR to /certsrc
# then download certnew.cer fron certsrv

require 'winrm'

conn = WinRM::Connection.new(
  endpoint: 'https://172.16.54.12:5986/wsman',
  transport: :ssl,
  client_cert: 'certnew.cer',
  client_key: 'privateKey.key',
  no_ssl_peer_verification: true
)

command=""

conn.shell(:powershell) do |shell|
    until command == "exit\n" do
        output = shell.run("-join($id,'PS ',$(whoami),'@',$env:computername,' ',$((gi $pwd).Name),'> ')")
        print(output.output.chomp)
        command = gets
        output = shell.run(command) do |stdout, stderr|
            STDOUT.print stdout
            STDERR.print stderr
        end
    end
    puts "Exiting with code #{output.exitcode}"
end
