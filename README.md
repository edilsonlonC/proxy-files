# proxy-pyzmq

<h1> Servidores de archivos </h1>

<p> Aplicación creada con pyzmq, consta de n servidores los cuales se pueden establecer el script /server/execute_server.sh un proxy que permite distribuir las partes de un archivo de manera equitativa en cada uno de los servidores y un cliente que consta de 4 comandos  </p>


<h3> Comandos para el cliente </h3>
 :arrow_right: register username <br>
:arrow_right: upload filename username <br>
:arrow_right: download filename username <br>
:arrow_right: list username <br>


<h4> Ejecutar programa </h4>
'''
git clone https://github.com/edilsonlonC/proxy-files.git <br>
cd proxy <br>
python main.py <br>
cd server <br>
./execute_server.sh <br>
cd client <br>
./client.py command <br>
'''

