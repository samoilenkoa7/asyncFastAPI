Generic single-database configuration.

# Usage

First of all, if you haven't file alembic.ini you should initialize migrations.
Using this command. 

      alembic init migrations

After that you will see folder with migrations and alembic CONF file.
1. In alembic.ini you should provide database url, for which you write migrations.
2. After that - open folder with migrations and indicate Base, or the name of
variable that calls `declarative_base()` function


      from myapp import myBase

3. After that input:


      alembic revision --autogenerate -m 'comment'


   And migration will be created

4. Finally input:
   
      
      `alembic upgrade heads`