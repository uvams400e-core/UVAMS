-- drop table `uvams-400e.mission_data.pluto_telemetry`;

CREATE OR REPLACE TABLE `uvams-400e.mission_data.pluto_telemetry` (
  timestamp TIMESTAMP,
  center_freq_hz FLOAT64,
  actual_freq_hz FLOAT64,        -- The real frequency detected
  doppler_shift_hz FLOAT64,     -- actual_freq - center_freq
  power_level FLOAT64,
  snr FLOAT64,
  bandwidth_hz FLOAT64,
  station_id STRING,
  event_type STRING,
  metadata JSON                 -- A "catch-all" for any extra data
)
PARTITION BY DATE(timestamp)
OPTIONS (
  partition_expiration_days = 14,
  description = "UVAMS Satellite Telemetry with Doppler and SNR tracking"
);

