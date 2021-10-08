from flask import Flask, request, Response
from flask_restful import Resource, Api
from Report import report
from dicttoxml import dicttoxml
from flasgger import Swagger


app = Flask(__name__)
api = Api(app)

swag = Swagger(app)


results = report.build_report('./data')


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
        rank = 0
        for r in results:
            rank += 1
            report_api[r.abbr_name] = {'rank': rank, 'name': r.name,
                                       'team': r.team, 'result': str(r.result)}
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
