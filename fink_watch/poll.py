# Copyright 2025 Julien Peloton
# Author: Julien Peloton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Get last alert offset"""

import confluent_kafka


def poll_last_offset(kafka_config, topic):
    """Return the last offset

    Parameters
    ----------
    kafka_config: dict
        Kafka consumer config
    topic: str
        Topic name

    Returns
    -------
    offsets: list
        Last offset
    """
    consumer = confluent_kafka.Consumer(kafka_config)
    topics = ["{}".format(topic)]
    consumer.subscribe(topics)

    metadata = consumer.list_topics(topic)
    if metadata.topics[topic].error is not None:
        raise confluent_kafka.KafkaException(metadata.topics[topic].error)

    # List of partitions
    partitions = [
        confluent_kafka.TopicPartition(topic, p)
        for p in metadata.topics[topic].partitions
    ]
    committed = consumer.committed(partitions)
    offset = 0
    for partition in committed:
        _, hi = consumer.get_watermark_offsets(partition, timeout=1, cached=False)
        offset += hi

    consumer.close()
    return offset
