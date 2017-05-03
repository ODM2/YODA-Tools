
import datetime
import copy
import yaml

class YamlPrinter():

    _references= {}
    def get_header(self, filetype):
        yoda_header = "---\n"
        yoda_header += "YODA:\n"

        yoda_header += " - {"
        yoda_header += "Version: \"{0}\", ".format("0.1.0")
        yoda_header += "Profile: \"{0}\", ".format(filetype)
        yoda_header += "CreationTool: \"{0}\", ".format("YodaConverter")
        yoda_header += "DateCreated: \"{0}\", ".format(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))
        yoda_header += "DateUpdated: \"{0}\"".format(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))
        yoda_header += "}\n"
        return yoda_header.replace('None', 'NULL')

    def handle_inheritance(self, apiobjs):
        # break into groups of object types (specimen vs site)
        from collections import defaultdict
        objlist = defaultdict(list)
        text = ""

        for obj in apiobjs:
            objlist[obj.__class__.__name__].append(obj)

        index = 0
        # call current function with each list, send in class name
        for k, v in objlist.items():
            text += self.print_objects(objlist[k],  index)
            index += len(objlist[k])
        return text

    def print_objects(self, apiobjs, ind = 0 ):
        # TODO handle inheritance objects
        objname = apiobjs[0].__class__.__name__

        text = objname + ":\n"

        index = 1 + ind
        for obj in apiobjs:

            primarykey = obj.__mapper__.primary_key[0].name
            valuedict = obj.__dict__.copy()

            #find the attribute name of the primary key
            for v in valuedict:
                if v.lower() == obj.__mapper__.primary_key[0].name:
                    # pop unwanted items from the dictionary
                    valuedict.pop(v)
                    if v != "BridgeID" and v != "RelationID":
                        primarykey = v
                    else:
                        #what to do if the primary key is BridgeID?
                        if objname[-1] == "s":
                            primarykey = objname[:-1] + "ID"
                        else:
                            primarykey = objname + "ID"
                    break

            #remove all id's from the dictionary
            for k in valuedict.keys():
                if "id" in k.lower() and "uuid" not in k.lower():
                    del valuedict[k]

            #assign the reference value for objects
            for key in dir(obj):
                if "obj" in key.lower():  # key.contains("Obj"):
                    try:
                        att = getattr(obj, key)
                        if att is not None:
                            valuedict[key] = self._references[att]
                        else:
                            valuedict[key] = "NULL"
                        #todo: featureaction, samplingfeatureobj not being found
                    except Exception as e:
                        print ("cannot find {} in {}. Error:{} in YamlPrinter".format(key, obj.__class__, e))

            self._references[obj] = '*{}{:0>4d}'.format(primarykey, index)
            text += ' - &{}{:0>4d} '.format(primarykey, index)
            text += self.print_dictionary(valuedict)
            index += 1
        return text

    def print_dictionary(self, dict):
        from numbers import Number
        final_string = "{"
        for k, v in dict.items():

            #if the item is null don't print it
            if v is None:
                final_string += '{}: NULL, '.format(k)
            elif isinstance(v, Number):
                final_string += '{}: {}, '.format(k, v)
            elif isinstance(v, basestring):
                if '*' in v:
                    final_string += '{}: {}, '.format(k, v)
                else:
                    final_string += '{}: "{}", '.format(k, v)
            elif isinstance(v, datetime.datetime) or isinstance(v, datetime.date):
                final_string += '{}: "{}", '.format(k, v.strftime("%Y-%m-%d %H:%M"))

        final_string = "{}}}\n".format(final_string[:-2])

        return final_string

    def add_to_db(self, objname, file, data):

        if objname in data:
            # check to see if this is an inherited object
            if data[objname][0].__class__ != data[objname][0]._sa_instance_state.key[0]:
                file.write(self.handle_inheritance(apiobjs=data[objname]))
            else:
                file.write(self.print_objects(data[objname]))

    def generate_ts_objects(self, data):


        return data.to_csv()

    def print_yoda(self, out_file, data):

        if "measurementresultvalues" in data:
            filetype = "SpecimenTimeSeries"
        else:
            filetype = "TimeSeries"

        with open(out_file, 'w') as yaml_schema_file:
            print data.keys()
            #header
            yaml_schema_file.write(self.get_header(filetype))
            #dataset
            self.add_to_db("datasets", yaml_schema_file, data)
            #organization
            self.add_to_db("organizations", yaml_schema_file, data)
            #people
            self.add_to_db("people", yaml_schema_file, data)
            #affiliations
            self.add_to_db("affiliations", yaml_schema_file, data)
            #citations
            self.add_to_db("citations", yaml_schema_file, data)
            #authorlists
            self.add_to_db("authorlists", yaml_schema_file, data)
            #datasetcitations
            self.add_to_db("datasetcitations", yaml_schema_file, data)
            #spatialreferences
            self.add_to_db("spatialreferences", yaml_schema_file, data)
            #samplingfeatures: Not explicitly printed, should be included in sites and specimen objects
            #sites
            # self.add_to_db("sites", yaml_schema_file, data)
            #specimens
            # self.add_to_db("specimens", yaml_schema_file, data)

            self.add_to_db("samplingfeatures", yaml_schema_file, data)
            #relatedfeatures
            self.add_to_db("relatedfeatures", yaml_schema_file, data)
            #units
            self.add_to_db("units", yaml_schema_file, data)
            #annotations
            self.add_to_db("annotations", yaml_schema_file, data)
            #methods
            self.add_to_db("methods", yaml_schema_file, data)
            #variables
            self.add_to_db("variables", yaml_schema_file, data)
            #proc level
            self.add_to_db("processinglevels", yaml_schema_file, data)
            #action
            self.add_to_db("actions", yaml_schema_file, data)
            #featureaction
            self.add_to_db("featureactions", yaml_schema_file, data)
            #actionby
            self.add_to_db("actionby", yaml_schema_file, data)
            #relatedActions
            self.add_to_db("relatedactions", yaml_schema_file, data)
            #result Not explicitly printed, should be included in measurement or timeseries results
            self.add_to_db("results", yaml_schema_file, data)
            # #measurement results
            # self.add_to_db("measurementresults", yaml_schema_file, data)
            # #timeseriesresult
            # self.add_to_db("timeseriesresults", yaml_schema_file, data)
            #datasetresults
            self.add_to_db("datasetsresults", yaml_schema_file, data)
            # measurementResultValues
            self.add_to_db("measurementresultvalues", yaml_schema_file, data)
            #timeseriesresultvalues - ColumnDefinitions:, Data:
            val = "timeseriesresultvalues"
            if val in data:
                yaml_schema_file.write(self.generate_ts_objects(data[val]))
            #MeasurementResultValueAnnotations
            self.add_to_db("measurementresultvalueannotations", yaml_schema_file, data)


            yaml_schema_file.write("...")

