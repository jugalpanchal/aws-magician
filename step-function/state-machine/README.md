- Synchronize Job - The resource is specified as elasticmapreduce:addStep.sync which is used to add a Step to an existing EMR cluster, and because we use .sync we are telling our state machine to submit the step and then wait until it completes before continuing.
- Asynchronize Job - 
