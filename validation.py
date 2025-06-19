import json
import logging 
class Validate_it_man:
    def __init__(self):
        pass

    def yaml_to_json(self,file):
        converted_file=[]
        return converted_file
    
    def print_report(self,report):
        validation_report=[]
        """

        True is set if error is found:

        """

        if(report['export_section'][0][1]==True):
            validation_report.append(['export_section',report['export_section']])
        else:
            validation_report.append(['export_section',"EXPORT looks Good :) no errors found!"])

        return validation_report
    
    def pretty_print(self,logs):
        print("By default you have opted to look for logs and explanation")
        print("\n")

        for i in logs:
            print("\n",i)
        
        print("\n")
            
    def spec(self,i_need="all"):
        ## yaml_to_json converter

        ## end of converter

        f=open("/Users/nitinsaimajji/Desktop/untitled folder/PROJECT-24/test.json","r")
        gotcha=json.loads(f.read())
        report={'load_section':[],'extract_section':[],'export_section':[]}

        # ## validate load section:
        # report['load_section'].append(self.load_checks(gotcha))


        # ## validate extract section:
        # report['extract_section'].append(self.extract_checks(gotcha))


        ## validate export section:
        report,error_logs,explanation = self.workflow_checks(gotcha)
        if(i_need=="report"):
            report['export_section'].append(report)
            return report
        elif(i_need=="error_logs"):
            return error_logs
        elif(i_need=="explanation"):
            return explanation
        elif(i_need=="all"):
            error_logs.extend(explanation)
            return error_logs


    def extract_check(self,gotcha):
        pass
    
    def export_checks(self,gotcha):
        pass

    def workflow_checks(self,gotcha):
        error_logs=[]
        explanation=[]
        report=[]
        worker_name=str(list(gotcha.keys())[0])
        # print("worker_name : ",worker_name)
        # print("gotcha[worker_name].keys() :",gotcha[worker_name].keys())
        if 'workflows' in gotcha[worker_name].keys():
            workflow_export_name='workflows' 
            workflow_export=gotcha[worker_name][workflow_export_name]
            # print("workflow_export_name :",workflow_export_name) ## event_export
            # print("workflow_export :", workflow_export.keys()) ## dict(['event_export'])

            event_export_name=str(list(workflow_export.keys())[0])
            ## assuming only 1 workflow
            event_export=workflow_export[event_export_name]
            # print("event_export.keys()",list(event_export.keys()))


            if 'params' in list(event_export.keys()):
                if(len(list(event_export['params'].keys()))==0) or 'run_freq_secs' not in list(event_export['params'].keys()):
                    error_logs.append(("ERROR: run_freq_secs is not set or missing in params"))
            else:
                error_logs.append(("ERROR: PARAMS section is missing"))


            if 'pipelines' in list(event_export.keys()):
                if(len(list(event_export['pipelines'].keys()))==1):
                    pipeline_export_name=str(list(event_export['pipelines'].keys())[0]) ## nlrm_metrics_data_ingest
                    # print("pipeline_export_name: ",pipeline_export_name)
                    pipeline_export=event_export['pipelines'][pipeline_export_name]
                    if(isinstance(pipeline_export,list)):
                        if(len(pipeline_export)<3):
                           error_logs.append(("ERROR: LESS THAN 3 entries Found in the Pipeline section in spec file"))
                        
                        validate_pipeline_section={'load':False,'extract':False,'export':False}
                        flag=True
                        for i in pipeline_export:
                            verify=i['job'].split(".")
                            if "load" in verify:
                                if(len(verify)==2 and verify[-1]=='load'):
                                    validate_pipeline_section['load']=flag
                                else:
                                    error_logs.append(("ERROR: Something wrong in LOAD in SECTION:PIPELINE"))
                            elif "extract" in verify:
                                if(len(verify)==2 and verify[-1]=='extract'):
                                    validate_pipeline_section['extract']=flag
                                else:
                                    error_logs.append(("ERROR: Something wrong in EXTRACT in SECTION:PIPELINE"))
                            elif "export" in verify:
                                if(len(verify)==3 and verify[-2]=='export'):
                                    if verify[-1] not in ['prometheus_remote_write','prometheus','mongo']:
                                        error_logs.append((f"ERROR: Found a invalid EXPORT method:[{verify[-1]}] in SECTION:PIPELINE > jobs"))

                                        explanation.append("The following are valid: ['prometheus_remote_write','prometheus','mongo']")
                                        validate_pipeline_section['export']=flag
                                elif(len(verify)==2):
                                    if verify[-1] not in ['prometheus_remote_write','prometheus','mongo']:
                                        error_logs.append((f"ERROR: Found a invalid EXPORT method:[{verify[-1]}] in SECTION: PIPELINE > jobs"))
                                        explanation.append("FIXES: The following are valid: ['metastore_info.export.prometheus']")
                                        explanation.append("FIXES: You can try other exports:['prometheus_remote_write','prometheus','mongo'] , prometheus_remote_write can be used if you have metrics and labels defined in the spec , or if you are only using labels then go with mongo")
                                        validate_pipeline_section['export']=flag
                                else:
                                    error_logs.append(("Something wrong in EXPORT in SECTION:PIPELINE"))

                        for key,value in validate_pipeline_section.items():
                            if(value==False):
                                error_logs.append((f"{key} section is missing from the SECTION:PIPELINE"))             
            else:
                error_logs.append(("ERROR: Piplines section is missing"))
        else:
            error_logs.append(("Workflows section is missing"))


        report.append(error_logs)
        if(len(error_logs)>0):
            report.append(True)
        else:
            report.append(False) 

        return [report,error_logs,explanation]


    def extract_chunks(self,chunk):
        pass

    def load_chunks(self,chunk):
        pass



v=Validate_it_man()
report=v.spec()
v.pretty_print(report)