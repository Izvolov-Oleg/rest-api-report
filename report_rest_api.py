from flask import Flask, request, Response
from flask_restful import Resource, Api
from dicttoxml import dicttoxml
from flasgger import Swagger
from models import *

app = Flask(__name__)
api = Api(app)

swag = Swagger(app)


class Report(Resource):

    def get(self):
        """
        Returns a list of drivers's report with format(json, xml) parameters
        ---
        summary: "Returns a list of drivers's report"
        description: "Returns a list of drivers's report"
        operationId: GetReport
        produces:
          - "application/xml"
          -  "application/json"
        tags:
          - Report
        parameters:
          - name: 'format'
            in: "query"
            enum:
              - 'json'
              - 'xml'
            required: true
        responses:
          200:
            description: "successful operation"
            schema:
              type: "object"
        """
        report_api = dict()
        with db:
            results = Racer.select()
            for r in results:
                report_api[r.abbr_name] = {
                    'name': r.name, 'team': r.team, 'result': str(r.result)}
        format_api = request.args.get('format')
        if format_api == "json":
            return report_api
        elif format_api == "xml":
            xml_report = dicttoxml(report_api)
            return Response(xml_report, content_type='text/xml')
        return "Format of report is not correct, please try again.", 405


api.add_resource(Report, '/api/v1/report/')

if __name__ == '__main__':
    app.run(debug=True)
