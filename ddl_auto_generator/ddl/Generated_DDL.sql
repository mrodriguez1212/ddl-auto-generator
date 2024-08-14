CREATE TABLE public.customers ( 
	 ID SERIAL PRIMARY KEY, 
	 customer_id varchar(200), 
	 first_name varchar(200), 
	 last_name varchar(200), 
	 email varchar(200), 
	 phone varchar(200) 
); 
 
CREATE TABLE public.orders ( 
	 ID SERIAL PRIMARY KEY, 
	 order_id varchar(200), 
	 customer_id varchar(200), 
	 order_date timestamp 
); 
 
CREATE TABLE public.order_product ( 
	 ID SERIAL PRIMARY KEY, 
	 order_id varchar(200), 
	 product_id varchar(200), 
	 quantity varchar(200) 
); 
 
CREATE TABLE public.products ( 
	 ID SERIAL PRIMARY KEY, 
	 product_id varchar(200), 
	 product_name varchar(200), 
	 in_stock varchar(200) 
); 
 
