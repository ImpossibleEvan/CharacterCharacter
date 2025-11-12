import client
import server

who = input("Are you the [s]erver or [c]lient? ").strip().lower()[0]

match who:
    case 's':
        server.main()
    case 'c':
        client.main()