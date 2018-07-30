from web import app
from datetime import datetime
from flask import render_template, jsonify, request
from web import DaaResponse
from web import DaaStatus
import logging
import requests
import json
import ontoDAA
from pprint import pprint

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', datetime=datetime)


@app.route('/table', methods=['GET'])
def getTable():
    args = request.args
    id = args.get('id', '_hidden__18_5_3_8db028d_1525188905526_888836_50183_pei')
    repository = args.get('repository', 'https://rdf4j.mind-tap.net/rdf4j-server/')
    repositoryId = args.get('repositoryid', 'mms')

# try {
#
#     SimpleDateFormat datetimeFormat = new SimpleDateFormat("yyyy_MM_dd_HH_mm_ss");
#     Timestamp timestamp = new Timestamp(System.currentTimeMillis());
#
#     String downloadFileName = String.format("table_%s.xlsx", datetimeFormat.format(timestamp));
#
#
#     response.setContentType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
#     response.setHeader(HttpHeaders.CONTENT_DISPOSITION,
#             "attachment; filename=\"" + downloadFileName + "\"");
#     //response.setContentLength(document.length());
#     response.setStatus(HttpStatus.CREATED.value());
#
#     getExcelTable(response.getOutputStream(), repository, repositoryId, id);
#
#     log.info("Table file {} downloaded", downloadFileName);
# } catch (SwtTableExtractorException | IOException e) {
#     log.error("Unable to return table", e);
# }


@app.route('/upload', methods=['GET'])
def upload():
    args = request.args
    source = args.get('source',
                      'http://rt168mms.serc.stevens.edu:8081/alfresco/service/projects/PROJECT-445e0f98-a6ba-4f8d-ba37-9fe807bae813/refs/master/elements')
    repository = args.get('repository', 'https://rdf4j.mind-tap.net/rdf4j-server/')
    repositoryId = args.get('repositoryid', 'mms')
    username = args.get('username', "")
    password = args.get('password', "")

    ret = DaaResponse.DaaResponse(DaaStatus.DaaStatus.FAIL.value, "not executed")

    logging.info("Received ingest request for json data from: %s to repository: %s/%s ", source, repository, repositoryId)

    result = "upload failed";

    #get element json
    if username and username.strip and password and password.strip:
        logging.info("Using authenticator with username:%s and password:%s", username, password)
        resp = requests.get(source, auth=(username, password))
    else:
        resp = requests.get(source)

    resp = requests.get(source, auth=(username, password))
    if resp.status_code == 200:
        parsed_json = json.loads(resp.text)
        project_id = parsed_json["elements"][0]["_projectId"]
        logging.info("Found _projectId: %s", project_id)
        #pprint(parsed_json)
        #print(parsed_json["elements"][0])
        #print(parsed_json["elements"][0]["_projectId"])
        #pprint(parsed_json["elements"][0])

        ## initialize the object
        A = ontoDAA.SysMLDAA(project_id)

        ## parse, map, and return excel document
        A.populateTripleStore(resp.text)

        ret = DaaResponse.DaaResponse(DaaStatus.DaaStatus.SUCCESS.value, "upload was successful");
        pass
    else:
        logging.error("Error getting connection to {}", source);
        ret = DaaResponse.DaaResponse(DaaStatus.DaaStatus.FAIL.value, "upload failed");

    return jsonify(ret.__dict__)
