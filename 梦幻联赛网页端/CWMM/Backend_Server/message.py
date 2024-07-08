from service import globalService


def message_server_match_status(servername):
    # 1 or 2
    return globalService.messageServerMatchStatus(servername)


def message_cancel_result(server, guids):
    return globalService.messageCancelMatch(server, guids)


def message_finish_result(server, data, s1, s2):
    return globalService.messageFinishMatch(server, data, s1, s2)


def message_show_server_message(index, msg: str):
    return "3|%d|%s" % (index, msg)


def message_kick_player(index):
    return "4|%d" % index


def message_ban_player_temporary(index):
    return "5|%d" % index


def message_broadcast_server_message(msg: str):
    return "6|%s" % msg


def message_player_status(servername, player_id, player_index):
    # 7
    return globalService.messagePlayerStatus(servername, player_id, player_index)
