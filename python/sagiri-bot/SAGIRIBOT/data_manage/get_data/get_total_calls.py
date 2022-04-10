from SAGIRIBOT.basics.aio_mysql_excute import execute_sql


async def get_total_calls(data_name: str) -> int:
    """
    Get function calls total count

    Args:
        data_name: Data to query
            data name list:
                setuCalled: Number of setu calls
                realCalled: Number of real calls
                bizhiCalled: Number of bizhi calls
                weatherCalled: Number of weather query calls
                responseCalled: Number of total calls
                clockCalled: Number of get time calls
                searchCount: Number of search img calls
                botSetuCount: Number of listen bot img calls
                dialsCount: Number of clock dials
                predictCount: Number of predict img calls
                yellowPredictCount: Number of yellow predict img calls
                quotesCount: Number of get quotes calls

    Examples:
        data = await get_total_calls("setuCalled")

    Return:
        int
    """
    data_name_dict = {
        "setu": "setuCalled",
        "real": "realCalled",
        "bizhi": "bizhiCalled",
        "weather": "weatherCalled",
        "response": "responseCalled",
        "clock": "clockCalled",
        "search": "searchCount",
        "botSetuCount": "botSetuCount",
        "predict": "predictCount",
        "yellow": "yellowPredictCount",
        "quotes": "quotesCount"
    }
    if data_name in data_name_dict.keys():
        sql = "SELECT %s from calledCount" % data_name_dict[data_name]
        await execute_sql(sql)
        data = await execute_sql(sql)
        return data[0][0]
    else:
        raise Exception("error: none operationType named %s!" % data_name)
