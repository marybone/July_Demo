# July_Demo
Provided one has a JSON element ready to go, the parsing, mapping, and excel writing  are accomplished with:
 
## initialize the object
A = SysMLDAA(project_id)
 
## parse, map, and return excel document
A.populateTripleStore(json_string)
 
The SysMLDAA class is a more specific version of a more general class with a few keywords and the like pre-written into the appropriate methods and a dedicated method that just runs the necessary steps for our demo one after another. Each call of the populateTripleStore method will re-run the full process and reflect any changes between the elements passed. This isn't a true "update" - I've just moved a couple lines of code around so that the object "forgets" the elements after writing the excel file. Obviously not what we want long term, but it'll let us replicate the last demo without having to worry about how exactly we want to do / track updates in the triple store. Also, the projectId is not particularly important right now - even if you feed in a blank string it won't change the results.
 
A warning - it's slow - both the parsing and mapping take a 2-3 minutes each. 

## Run Demo
./RuneDemoEnv/bin/activate

### development notes
Please keep in mind that the Project ID is absolutely necessary to get the latest json data out of MMS.
It is still the same as before: “PROJECT-445e0f98-a6ba-4f8d-ba37-9fe807bae813” with the ref id “master”.
