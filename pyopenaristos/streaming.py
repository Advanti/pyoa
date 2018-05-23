import kafka
import json
import uuid


def _kafka_get_producer(server):
    return kafka.KafkaProducer(
        bootstrap_servers=server,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'))


def _command_submit(server, payload, topic='oa.command'):
    producer = _kafka_get_producer(server)
    if not producer:
        raise RuntimeError('failed to obtain kafka producer')

    try:
        producer.send(topic, payload)
        producer.flush()
        producer.close()
    except Exception as exc:
        raise RuntimeError('failed to submit command: %s'.format(exc))


def topology_launch(server, name, arguments):
    tx = str(uuid.uuid4())[0:8]

    _command_submit(server, {
        'action': 'launch_topology',
        'parameters': {
            'name': name,
            'arguments': arguments
        },
        'tx': tx
    })

    return {
        'host': server,
        'tx': tx,
        'topics': [
            'oa.custom.{0}'.format(tx),
        ]
    }


def topology_consume(server, knowledge, topic='streaming.twitter'):
    topic = topic + '.' + knowledge
    consumer = kafka.KafkaConsumer(topic, bootstrap_servers=server)

    for msg in consumer:
        yield msg.value


def topology_consume_custom(server, tx, knowledge):
    topic = 'oa.custom.{0}.{1}'.format(tx, knowledge)

    consumer = kafka.KafkaConsumer(topic, bootstrap_servers=server)

    for msg in consumer:
        yield msg.value


def topology_kill(server, tx):
    ttx = str(uuid.uuid4())[0:8]

    _command_submit(server, {
        'action': 'kill_topology',
        'parameters': {
            'tx': tx,
        },
        'tx': ttx,
    })

    return {
        'host': server,
        'tx': ttx,
    }