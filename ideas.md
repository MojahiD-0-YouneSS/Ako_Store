{ shose, cart , enter user info , shop}

# 1:
profile{admin_use}

# 2:
contact: +
 {name, phone, city, email (optional)}

# 2:
contact: +
 social media

# 3:
  cart + shoping history

# 4:
coversation

# 5:
authorisation authentication

# 6:
localisation

# 7:
categorisation

# 8:
headlines

# 9:
payment online / cash on delivery


//

1) button  for whole outfit , still needs fixing
2) forgot email/password x, needs costom 
3) passwords:
  admin: 'Tizguin1akbor'
  we: '789qwe123zxc'
4)  fix outfit view names to side and pic are too close x
5) adverts linked to a product when it's been promoted x
6) search features:
  *product name -> 1 or x
  *category  -> x
  *subcategory -> x
  *tags -> x
  *search tags: -> x
  *price: -> integral [x, y]
7) none regestred clients x
8) more info
9) order x
10) review
11) comunication with seller
12) online payment
13) wish list

**structure**:
  *dtg flag args path*
# dtg -hf: (class a) flag

function [spd], args = [3], staitic_arg = [1], dynamic_args = [2],
function [eld], args = [2], staitic_arg = [1], dynamic_args = [1],
function [dsd], args = [2], staitic_arg = [1], dynamic_args = [1],
function [vld], args = [1], staitic_arg = [0], dynamic_args = [1],
function [sbd], args = [3], staitic_arg = [0], dynamic_args = [3],
function [mdsd], args = [2], staitic_arg = [1], dynamic_args = [1],
function [dfcd], args = [6], staitic_arg = [0], dynamic_args = [6],
function [fdv], args = [3], staitic_arg = [3], dynamic_args = [0],

# dtg -sf: (class b) flag

function [ds], args = [2], staitic_arg = [1], dynamic_args = [1],
function [dsa], args = [3], staitic_arg = [2], dynamic_args = [1],
function [df], args = [6], staitic_arg = [2], dynamic_args = [4],
function [dg], args = [8], staitic_arg = [7], dynamic_args = [1],
function [dao], args = [16], staitic_arg = [12], dynamic_args = [4],

# dtg : (if no flag the function dao is called with it's ags)
hidden function [dao], args = [16], staitic_arg = [12], dynamic_args = [4],

3 weeks


order ==> client ==> regestred ==> y --> n
poster == 4 images

work on sections with fillters:
section page:
marks
products
number of products
give the admin/staf controll over reviews and users accounts

fabric = done
product details
outfit selector 
payment # cannceled?
cancell order = done
review control

canncell order? 
order => (
  add order.quantity to product.quantity,
  add logs to client (canncelled order)
)

all_in_one:

size -> quantity

brand -> reference_number

fabric -> reference_number


**********************************************************

for user:
landing page: --> show products
             --> user input
             --> among wannted
admin : --> add products
        --> takes orders
        --> valide | canncel
        --> telecharger pdf (user info / content purchesed) 


view_functiom :


rachid : user = User.objects.create_user(username='youness', email='staff@example.com', password='password123')**********************************************************