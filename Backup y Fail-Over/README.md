El documento a continuacion tiene como objetivo la explicacion de la herramienta y el funcionamiento de Barman
que permite realizar backup y fail-over.

Barman es una herramienta especialmente creada para realizar backups remotos a una base de datos PostgreSQL,
lo cual lo realiza a travez de comunicacion SSH y con la ayuda del comando rsync. Donde a continuacion veremos
un ejemplo implementado por nosotros.

Primero como podemos observar hay 2 maquinas virtuales, una llamada "Barman Copia", en la cual se encuentra
instalado barman y es quien solicitara hacer los backups, cuya direccion dentro de la red virtual es
"176.16.143.130", la otra maquina virtual se llama "BD Principal" cuya direccion dentro de la red virtual es
"176.16.143.131", es quien almacena la base de datos principal PostgreSQL y es a quien se le solicitaran
poder realizar los backups.

A continuacion se muestran las tabla de la base de datos en cuestion llamada "distribuidos".

![1](https://user-images.githubusercontent.com/22055735/33243458-7bfef568-d2c5-11e7-9c41-df4d6db25008.png)

Ahora en la otra maquina podemos revisar la lista de backups anteriores a travez del comando
"barman list-backup main", donde "main" es el nombre que se le dio a la conexion con la base de
datos "distribuidos", como se puede observar todos estos tienen un ID formado por el formato
*fecha*T*hora* y a continuacion dia y hora de cuando se realizo. Ahora a traves del
comando "barman backup main" se le solicita a barman realizar un backup de la base de datos "distribuidos",
donde una vez realizado se pueden solicitar la lista de backup para esta base de datos y se puede observar
el nuevo backup realizado recientemente.

![2](https://user-images.githubusercontent.com/22055735/33243459-7c2eb212-d2c5-11e7-92c6-7d61429426c8.png)

Ahora entonces se simulara un desastre que tiene como consecuencia que las tablas "customer" y "lineitem" de la
base de datos son eliminadas, proceso que se realiza con los comandos "DROP TABLE" como se muestra a continuacion:

![3](https://user-images.githubusercontent.com/22055735/33243460-7c50e51c-d2c5-11e7-891e-e8322fa62d63.png)

Entonces una vez que se haya dado cuenta de este error, se detiene el servicio de la base de datos, y ahora
barman debe encargarse de mandar a recuperar la base de datos, ahora mostrando los detalles del ultimo backup
realizado a traves del comando "barman show-backup main latest" para obtener la fecha de inicio del backup.
Se utilizara el comando "recover" para mandar a recuperar la base de datos en la maquina virtual
"BD Principal" en base al ultimo backup realizado, el comando recover utiliza varios parametros, entre ellos
la fecha de inicio del backup, la direccion de la maquina virtual de la base de datos, la conexion co nella
y el ID del backup, "barman recover --target-time "Begin time"  --remote-ssh-command
"ssh postgres@standby-db-server-ip"   main-db-server   backup-id   /var/lib/pgsql/9.4/data".

![4](https://user-images.githubusercontent.com/22055735/33243461-7c6fb104-d2c5-11e7-9ea9-dc565b92e73f.png)

Ahora una vez ejecuta el comando:

![5](https://user-images.githubusercontent.com/22055735/33243462-7c8eeba0-d2c5-11e7-8aa1-797b17623b76.png)

Se inician los servicios de postgresql nuevamente en la maquina y se consulta las tablas, pudiendo observar que
el contenido de la base de datos distribuidos se ha podido recuperar satisfactoriamente

![6](https://user-images.githubusercontent.com/22055735/33243463-7cada978-d2c5-11e7-9e36-ca47b5207378.png)