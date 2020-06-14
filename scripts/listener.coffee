module.exports = (robot) ->

    console.log "Bot online."
    
    robot.hear new RegExp(
        '^compare\s*$',
        'i'
    ), (response) ->

        ## Get raw message

        raw = response.message.rawMessage
        console.log raw

        ## prepare basic parameters

        channel = raw.channel
        requester_name = raw.user.name
        timestamp = raw.event_ts
        command = raw.text

        ## build parameters
        getparams = command

        ## pass request to worker
        #response.message.thread_ts = raw.ts
        response.send "*Comparing with previous day's record...*"

        console.log "Sending to worker: /" + getparams
        robot.http("http://localhost:5151/" + getparams).get() (err, httpresponse, body) ->
            console.log "err: " + err
            console.log "response: " + httpresponse
            console.log "body: " + body
            response.send body
