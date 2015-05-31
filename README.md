# LOD-Identity-checker
Identity checker for linked open data

#Services
- find connected concepts
- estimate likelihood of coinciding identity

#To do
- count datapoints containing sameAs statements in LOD laundromat
- create RESTful API endpoint to allow querying
- design reliability metric

#To deploy:

-Requirements:
- Tomcat Server (included in XAMPP, or seperate install)]
- OpenRDF Sesame Triple store
- Flask

-Actions:
- Put Sesame .war files in Tomcats Webapps folder
- Start Tomcat and navigate to tomcat in browser (on localhost:8080/openrdf-workbench (or different server))
- Create OWLIM-Lite repository named "AR-AI" using identity.nq and OWL2-RL reasoning framework.
- Start api.py using python and navigate to localhost:5000/api/identity?uri="##used URI##" or localhost:5000/api/compare?uri1=##first URI##&uri2=##second URI## to query, or use interface (limited) by going to localhost:5000.  

