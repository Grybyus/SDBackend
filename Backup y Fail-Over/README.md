El documento a continuación tiene como objetivo la explicación de la herramienta y el funcionamiento de Barman
que permite realizar backup y fail-over.

![logo1](https://user-images.githubusercontent.com/22055735/33243504-4c28be7c-d2c6-11e7-9f0e-3e5a23ff6b35.png)

Barman es una herramienta especialmente creada para realizar backups remotos a una base de datos PostgreSQL,
lo cual lo realiza a través de comunicación SSH y con la ayuda del comando rsync. Donde a continuación veremos
un ejemplo implementado por nosotros.

Primero como podemos observar hay 2 maquinas virtuales, una llamada "Barman Copia", en la cual se encuentra
instalado barman y es quien solicitara hacer los backups, cuya dirección dentro de la red virtual es
"176.16.143.130", la otra maquina virtual se llama "BD Principal" cuya dirección dentro de la red virtual es
"176.16.143.131", es quien almacena la base de datos principal PostgreSQL y es a quien se le solicitarán
poder realizar los backups.

A continuación se muestran las tabla de la base de datos en cuestión llamada "distribuidos".

![1](https://user-images.githubusercontent.com/22055735/33243458-7bfef568-d2c5-11e7-9c41-df4d6db25008.png)

Ahora en la otra máquina podemos revisar la lista de backups anteriores a través del comando
"barman list-backup main", dónde "main" es el nombre que se le dio a la conexión con la base de
datos "distribuidos", como se puede observar todos estos tienen un ID formado por el formato
*fecha*T*hora* y a continuación día y hora de cuando se realizó. Ahora a través del
comando "barman backup main" se le solicita a barman realizar un backup de la base de datos "distribuidos",
donde una vez realizado se pueden solicitar la lista de backup para esta base de datos y se puede observar
el nuevo backup realizado recientemente.

![2](https://user-images.githubusercontent.com/22055735/33243459-7c2eb212-d2c5-11e7-92c6-7d61429426c8.png)

Ahora entonces se simulara un desastre que tiene como consecuencia que las tablas "customer" y "lineitem" de la
base de datos son eliminadas, proceso que se realiza con los comandos "DROP TABLE" como se muestra a continuación:

![3](https://user-images.githubusercontent.com/22055735/33243460-7c50e51c-d2c5-11e7-891e-e8322fa62d63.png)

Entonces una vez que se haya dado cuenta de este error, se detiene el servicio de la base de datos, y ahora
barman debe encargarse de mandar a recuperar la base de datos, ahora mostrando los detalles del último backup
realizado a través del comando "barman show-backup main latest" para obtener la fecha de inicio del backup.
Se utilizará el comando "recover" para mandar a recuperar la base de datos en la máquina virtual
"BD Principal" en base al último backup realizado, el comando recover utiliza varios parámetros, entre ellos
la fecha de inicio del backup, la dirección de la máquina virtual de la base de datos, la conexión con ella
y el ID del backup, "barman recover --target-time "Begin time"  --remote-ssh-command
"ssh postgres@standby-db-server-ip"   main-db-server   backup-id   /var/lib/pgsql/9.4/data".

![4](https://user-images.githubusercontent.com/22055735/33243461-7c6fb104-d2c5-11e7-9ea9-dc565b92e73f.png)

Ahora una vez ejecuta el comando:

![5](https://user-images.githubusercontent.com/22055735/33243462-7c8eeba0-d2c5-11e7-8aa1-797b17623b76.png)

Se inician los servicios de postgresql nuevamente en la máquina y se consulta las tablas, pudiendo observar que
el contenido de la base de datos distribuidos se ha podido recuperar satisfactoriamente

![6](https://user-images.githubusercontent.com/22055735/33243463-7cada978-d2c5-11e7-9e36-ca47b5207378.png)

Finalmente como se puede observar el backup puede ser realizado a través de un solo comando, por lo cual
utilizando cron el cual es un ejecutador de tarea en segundo plano, se puede configurar que este comando
de backup sea ejecutado a ciertas horas, días, meses, etc.

![cron](https://user-images.githubusercontent.com/22055735/33244084-b8590f9e-d2cf-11e7-9fda-00595a634eac.jpg)

Donde ejecutando el comando "crontab -e" se abre la lista para configurar comandos por el usuario, y a
continuación se configura la ejecución cada 1 min.

![9](https://user-images.githubusercontent.com/22055735/33244090-cce8812e-d2cf-11e7-9e27-eaffe17c753f.png)

Y ahora esperando unos minutos para observar resultados:

![10](https://user-images.githubusercontent.com/22055735/33244091-cd1f0898-d2cf-11e7-8277-f65b822e4ef7.png)


