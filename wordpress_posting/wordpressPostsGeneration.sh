#!/bin/sh
rm ScheduleCat.py
touch ScheduleCat.py

echo "#!/usr/bin/python" >> ScheduleCat.py
echo "# -*- coding: iso-8859-15 -*-" >> ScheduleCat.py

echo "from wordpress_xmlrpc import Client, WordPressPost" >> ScheduleCat.py
echo "from wordpress_xmlrpc.methods.posts import GetRecentPosts, NewPost" >> ScheduleCat.py
echo "from wordpress_xmlrpc.methods.users import GetUserInfo" >> ScheduleCat.py

echo "wp = Client('http://www.wordpressblog.com/xmlrpc.php', 'yourWordpressUser', 'yourWordpressPassword')" >> ScheduleCat.py

var=`cat comentarios`
count=0
data_ini=1
data_fin=9
mes=11
any=2011
data=$data_ini

echo " "  >> ScheduleCat.py

echo " "  >> ScheduleCat.py

for i in $var; do
	echo "post"$count" = WordPressPost()" >> ScheduleCat.py
	
	post_var_category=`echo "$i" | sed 's/\(.*\)..../\1/' | sed 's/\(.*\)........................../\1/' |  sed 's,-, ,' |sed 's,-, ,' |sed 's,-, ,' |sed 's,-, ,' | sed 's,-, ,' | sed 's,-, ,' | sed 's,-, ,'| sed 's,-, ,'| sed 's,-, ,'| sed 's,-, ,'`
	post_var_normal=`echo "$i" |  sed 's/\(.*\)..../\1/' | sed 's,-, ,' |sed 's,-, ,' |sed 's,-, ,' |sed 's,-, ,' | sed 's,-, ,' | sed 's,-, ,' | sed 's,-, ,'| sed 's,-, ,'| sed 's,-, ,'| sed 's,-, ,' | sed 's/\([a-z]\)\([a-zA-Z0-9]*\)/\u\1\2/g'`

	echo $post_var_category

	echo "post"$count".title = '"$post_var_normal" - Avenida Sarriá 17 de Barcelona'" >> ScheduleCat.py
	echo "post"$count".description = '<center><a href=\"http://www.mitorestaurant.com/images/thumb/local.JPG\"><img src=\"http://www.mitorestaurant.com/images/thumb/local.JPG\" alt=\"$post_var_normal - Restaurante Asiático Mito Barcelona - Avinguda Sarriá 17 Barcelona - Reservas al 93 410 94 93\"></a></center><br>Estamos hablando de <a href=\"http://www.mitorestaurant.com/comentarios/$i\">$post_var_normal</a> del restaurante Asiático Mito Cocina Asiática en la Avenida Sarriá 17 de Barcelona<br>Preguntas y reservas para catar este restaurante en el número 93 410 94 93 <br><a href=\"http://www.mitorestaurant.com/comentarios/\">"$post_var_normal" y aún más criticas como esta del Restaurante Mito Cocina Asiática de Barcelona</a><br>'" >> ScheduleCat.py
	echo "post"$count".tags = '$post_var_category'" >> ScheduleCat.py
	echo "post"$count".categories = ['menu degustacion','menu para 2','menu para dos','$post_var_category']" >> ScheduleCat.py
	
	rand_hora=`dd if=/dev/urandom count=1 2> /dev/null | cksum | cut -f1 -d" "`
	hora=$((($rand_hora % 12) + 10))
	rand_minut=`dd if=/dev/urandom count=1 2> /dev/null | cksum | cut -f1 -d" "`	
	minut=$((($rand_minut % 50)+10))
	rand_minut=`dd if=/dev/urandom count=1 2> /dev/null | cksum | cut -f1 -d" "`
	segon=$((($rand_minut % 50)+10))


	echo "post"$count".date_created = '$any"$mes"0"$data"T"$hora":"$minut":"$segon"'" >> ScheduleCat.py

	echo "wp.call(NewPost(post"$count", True))" >> ScheduleCat.py
	count=`expr $count + 1`	
	data=`expr $data + 1`	
	
	
	if [ "$data" -gt "$data_fin" ]
	then
	data=$data_ini	
	fi

	echo " "  >> ScheduleCat.py

	echo " "  >> ScheduleCat.py
done
