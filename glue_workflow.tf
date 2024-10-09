data "aws_caller_identity" "current" {}


resource "aws_glue_workflow" "CaseWorkflow" {
    name = "workflow_ing_api_case"
    default_run_properties = {
      
    }

    tags = {
      key = ""
    }
  
}

resource "aws_glue_trigger" "TriggerJobIni" {
    name = "Trigger_jo"
    type = "ON_DEMAND"
    workflow_name = aws_glue_workflow.CaseWorkflow.name
    depends_on = [ aws_glue_workflow.CaseWorkflow ]
    actions {
      job_name = "job_ini"
    }
    tags = {
      key = ""
    }
}

resource "aws_glue_trigger" "TriggerJobIni" {
    name = "Trigger_jo"
    type = "CONDITIONAL"
    workflow_name = aws_glue_workflow.CaseWorkflow.name
    depends_on = [ aws_glue_workflow.CaseWorkflow ]
    actions {
      job_name = "job_ini"
    }
    tags = {
      key = ""
    }
}