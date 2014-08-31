import argparse

from pythonosc import osc_message_builder
from pythonosc import udp_client


def send_msg(client, address, *args):
    msg = osc_message_builder.OscMessageBuilder(address=address)
    for arg in args:
        msg.add_arg(arg)
    client.send(msg.build())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', default='127.0.0.1', help='The ip of the OSC server')
    parser.add_argument('--passcode', type=str, default=None, help='The passcode to use for connecting to QLab')
    parser.add_argument('file', nargs='?', help='The file to read titles from')
    args = parser.parse_args()

    client = udp_client.UDPClient(args.server, 53000)

    if args.passcode is not None:
        send_msg(client, '/connect', args.passcode)
    else:
        send_msg(client, '/connect')

    file = open(args.file)

    last_cue = 0
    last_blank = True
    last_titles_was_decimal = False
    for line in file.readlines():
        line = line[:-1]
        this_cue = last_cue + 1
        this_blank = line == '.'
        broken_line = line.replace('/', '\n')
        if not last_blank:
            send_msg(client, '/new', 'stop')
            send_msg(client, '/cue/selected/number', str(this_cue))
            send_msg(client, '/cue/selected/cueTargetNumber',
                     str(last_cue) + '.1' if last_titles_was_decimal else str(last_cue))
            send_msg(client, '/cue/selected/name', 'BLANK' if this_blank else line)
            if not this_blank:
                send_msg(client, '/cue/selected/continueMode', 1)
        if not this_blank:
            send_msg(client, '/new', 'titles')
            send_msg(client, '/cue/selected/number', str(this_cue) + '.1' if not last_blank else str(this_cue))
            send_msg(client, '/cue/selected/text', broken_line)
            send_msg(client, '/cue/selected/name', line if last_blank else '--')
        last_cue = this_cue
        last_titles_was_decimal = not last_blank
        last_blank = this_blank

    send_msg(client, '/disconnect')


if __name__ == '__main__':
    main()