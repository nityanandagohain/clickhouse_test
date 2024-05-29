Two clusters of ClickHouse created

* clickhouse-1 is connected to nitya-1 bucket - prefer_not_to_merge=0
* clickhouse-2 is connected to nitya-2 bucket - prefer_not_to_merge=1


We are also setting support_batch_delete to false, because GCS doesn’t support batch delete, not sure if it will affect with no. of delete request between S3 and GCS.

```
CREATE TABLE default.test(
    timestamp UInt64 CODEC(DoubleDelta, LZ4),
    data String
)
ENGINE = MergeTree
PARTITION BY toDate(timestamp/1000000000)
ORDER BY (timestamp)
TTL toDateTime(timestamp / 1000000000) + toIntervalSecond(259200), toDateTime(timestamp / 1000000000) + toIntervalSecond(172800) TO VOLUME 's3'
SETTINGS index_granularity = 8192, ttl_only_drop_parts = 1, storage_policy = 'tiered'
    








SELECT
    disk_name,
    database,
    table,
    formatReadableSize(sum(data_compressed_bytes) AS size) AS compressed,
    formatReadableSize(sum(data_uncompressed_bytes) AS usize) AS uncompressed,
    round(usize / size, 2) AS compr_rate,
    sum(rows) AS rows,
    count() AS part_count
FROM system.parts
WHERE (active = 1) AND (table LIKE '%test%')
GROUP BY
    disk_name,
    database,
    table
ORDER BY
    disk_name ASC,
    size DESC