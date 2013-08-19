
import cgi 
import cgitb; cgitb.enable() 
import athletemodel
import yate


print(yate.start_response())
print(yate.include_header("this is Normal Google search result page"))