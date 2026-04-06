---
title: "reference documentation"
source: "https://libtorrent.org/reference.html"
---

# reference documentation

[single-page version](single-page-ref.md)

Torrent Handle

[block\_info](reference-Torrent_Handle.md#block_info)

[partial\_piece\_info](reference-Torrent_Handle.md#partial_piece_info)

[torrent\_handle](reference-Torrent_Handle.md#torrent_handle)

[hash\_value()](reference-Torrent_Handle.md#hash_value())

Session

[session\_proxy](reference-Session.md#session_proxy)

[session](reference-Session.md#session)

[session\_params](reference-Session.md#session_params)

[session\_handle](reference-Session.md#session_handle)

[write\_session\_params()](reference-Session.md#write_session_params())

[read\_session\_params()](reference-Session.md#read_session_params())

[write\_session\_params\_buf()](reference-Session.md#write_session_params_buf())

Stats

[counters](reference-Stats.md#counters)

[stats\_metric](reference-Stats.md#stats_metric)

[session\_stats\_metrics()](reference-Stats.md#session_stats_metrics())

[find\_metric\_idx()](reference-Stats.md#find_metric_idx())

[metric\_type\_t](reference-Stats.md#metric_type_t)

Core

[peer\_request](reference-Core.md#peer_request)

[peer\_info](reference-Core.md#peer_info)

[info\_hash\_t](reference-Core.md#info_hash_t)

[piece\_block](reference-Core.md#piece_block)

[load\_torrent\_file()](reference-Core.md#load_torrent_file())

[load\_torrent\_buffer()](reference-Core.md#load_torrent_buffer())

[load\_torrent\_parsed()](reference-Core.md#load_torrent_parsed())

[torrent\_peer\_equal()](reference-Core.md#torrent_peer_equal())

[make\_magnet\_uri()](reference-Core.md#make_magnet_uri())

[parse\_magnet\_uri()](reference-Core.md#parse_magnet_uri())

[version()](reference-Core.md#version())

[truncate\_files()](reference-Core.md#truncate_files())

[event\_t](reference-Core.md#event_t)

[socket\_type\_t](reference-Core.md#socket_type_t)

[connection\_type](reference-Core.md#connection_type)

[portmap\_transport](reference-Core.md#portmap_transport)

[portmap\_protocol](reference-Core.md#portmap_protocol)

[protocol\_version](reference-Core.md#protocol_version)

[int](reference-Core.md#int)

[download\_priority\_t](reference-Core.md#download_priority_t)

[char const\*](reference-Core.md#charconst*)

[std::uint64\_t](reference-Core.md#std::uint64_t)

[pex\_flags\_t](reference-Core.md#pex_flags_t)

[torrent\_flags\_t](reference-Core.md#torrent_flags_t)

Add Torrent

[client\_data\_t](reference-Add_Torrent.md#client_data_t)

[add\_torrent\_params](reference-Add_Torrent.md#add_torrent_params)

Settings

[overview](reference-Settings.md#overview)

[settings\_pack](reference-Settings.md#settings_pack)

[min\_memory\_usage()](reference-Settings.md#min_memory_usage())

[high\_performance\_seed()](reference-Settings.md#high_performance_seed())

[name\_for\_setting()](reference-Settings.md#name_for_setting())

[setting\_by\_name()](reference-Settings.md#setting_by_name())

[default\_settings()](reference-Settings.md#default_settings())

[generate\_fingerprint()](reference-Settings.md#generate_fingerprint())

Torrent Status

[torrent\_status](reference-Torrent_Status.md#torrent_status)

Trackers

[announce\_infohash](reference-Trackers.md#announce_infohash)

[announce\_endpoint](reference-Trackers.md#announce_endpoint)

[announce\_entry](reference-Trackers.md#announce_entry)

Torrent Info

[web\_seed\_entry](reference-Torrent_Info.md#web_seed_entry)

[load\_torrent\_limits](reference-Torrent_Info.md#load_torrent_limits)

[torrent\_info](reference-Torrent_Info.md#torrent_info)

DHT

[dht\_state](reference-DHT.md#dht_state)

[dht\_storage\_counters](reference-DHT.md#dht_storage_counters)

[dht\_storage\_interface](reference-DHT.md#dht_storage_interface)

[dht\_default\_storage\_constructor()](reference-DHT.md#dht_default_storage_constructor())

[sign\_mutable\_item()](reference-DHT.md#sign_mutable_item())

[announce\_flags\_t](reference-DHT.md#announce_flags_t)

Resume Data

[read\_resume\_data()](reference-Resume_Data.md#read_resume_data())

[write\_resume\_data()](reference-Resume_Data.md#write_resume_data())

[write\_resume\_data\_buf()](reference-Resume_Data.md#write_resume_data_buf())

[write\_torrent\_file\_buf()](reference-Resume_Data.md#write_torrent_file_buf())

[write\_torrent\_file()](reference-Resume_Data.md#write_torrent_file())

[write\_torrent\_flags\_t](reference-Resume_Data.md#write_torrent_flags_t)

Bencoding

[overview](reference-Bencoding.md#overview)

[entry](reference-Bencoding.md#entry)

[operator<<()](reference-Bencoding.md#operator<<())

[bencode()](reference-Bencoding.md#bencode())

Filter

[ip\_filter](reference-Filter.md#ip_filter)

[port\_filter](reference-Filter.md#port_filter)

Create Torrents

[overview](reference-Create_Torrents.md#overview)

[create\_torrent](reference-Create_Torrents.md#create_torrent)

[add\_files()](reference-Create_Torrents.md#add_files())

[set\_piece\_hashes()](reference-Create_Torrents.md#set_piece_hashes())

Bdecoding

[bdecode\_node](reference-Bdecoding.md#bdecode_node)

[print\_entry()](reference-Bdecoding.md#print_entry())

[bdecode()](reference-Bdecoding.md#bdecode())

Error Codes

[storage\_error](reference-Error_Codes.md#storage_error)

[gzip\_category()](reference-Error_Codes.md#gzip_category())

[pcp\_category()](reference-Error_Codes.md#pcp_category())

[bdecode\_category()](reference-Error_Codes.md#bdecode_category())

[libtorrent\_category()](reference-Error_Codes.md#libtorrent_category())

[http\_category()](reference-Error_Codes.md#http_category())

[i2p\_category()](reference-Error_Codes.md#i2p_category())

[socks\_category()](reference-Error_Codes.md#socks_category())

[upnp\_category()](reference-Error_Codes.md#upnp_category())

[error\_code\_enum](reference-Error_Codes.md#error_code_enum)

[pcp\_errors](reference-Error_Codes.md#pcp_errors)

[error\_code\_enum](reference-Error_Codes.md#error_code_enum)

[error\_code\_enum](reference-Error_Codes.md#error_code_enum)

[http\_errors](reference-Error_Codes.md#http_errors)

[i2p\_error\_code](reference-Error_Codes.md#i2p_error_code)

[socks\_error\_code](reference-Error_Codes.md#socks_error_code)

[error\_code\_enum](reference-Error_Codes.md#error_code_enum)

Custom Storage

[overview](reference-Custom_Storage.md#overview)

[disk\_observer](reference-Custom_Storage.md#disk_observer)

[buffer\_allocator\_interface](reference-Custom_Storage.md#buffer_allocator_interface)

[disk\_buffer\_holder](reference-Custom_Storage.md#disk_buffer_holder)

[settings\_interface](reference-Custom_Storage.md#settings_interface)

[open\_file\_state](reference-Custom_Storage.md#open_file_state)

[disk\_interface](reference-Custom_Storage.md#disk_interface)

[storage\_holder](reference-Custom_Storage.md#storage_holder)

[file\_open\_mode\_t](reference-Custom_Storage.md#file_open_mode_t)

Utility

[hasher](reference-Utility.md#hasher)

[hasher256](reference-Utility.md#hasher256)

[bitfield](reference-Utility.md#bitfield)

Plugins

[overview](reference-Plugins.md#overview)

[peer\_connection\_handle](reference-Plugins.md#peer_connection_handle)

[bt\_peer\_connection\_handle](reference-Plugins.md#bt_peer_connection_handle)

[plugin](reference-Plugins.md#plugin)

[torrent\_plugin](reference-Plugins.md#torrent_plugin)

[peer\_plugin](reference-Plugins.md#peer_plugin)

[crypto\_plugin](reference-Plugins.md#crypto_plugin)

[create\_smart\_ban\_plugin()](reference-Plugins.md#create_smart_ban_plugin())

[create\_ut\_pex\_plugin()](reference-Plugins.md#create_ut_pex_plugin())

[create\_ut\_metadata\_plugin()](reference-Plugins.md#create_ut_metadata_plugin())

Storage

[storage\_params](reference-Storage.md#storage_params)

[file\_slice](reference-Storage.md#file_slice)

[file\_storage](reference-Storage.md#file_storage)

[mmap\_disk\_io\_constructor()](reference-Storage.md#mmap_disk_io_constructor())

[default\_disk\_io\_constructor()](reference-Storage.md#default_disk_io_constructor())

[disabled\_disk\_io\_constructor()](reference-Storage.md#disabled_disk_io_constructor())

[posix\_disk\_io\_constructor()](reference-Storage.md#posix_disk_io_constructor())

[storage\_mode\_t](reference-Storage.md#storage_mode_t)

[status\_t](reference-Storage.md#status_t)

[move\_flags\_t](reference-Storage.md#move_flags_t)

PeerClass

[peer\_class\_info](reference-PeerClass.md#peer_class_info)

[peer\_class\_type\_filter](reference-PeerClass.md#peer_class_type_filter)

ed25519

[ed25519\_create\_seed()](reference-ed25519.md#ed25519_create_seed())

[ed25519\_create\_keypair()](reference-ed25519.md#ed25519_create_keypair())

[ed25519\_sign()](reference-ed25519.md#ed25519_sign())

[ed25519\_verify()](reference-ed25519.md#ed25519_verify())

[ed25519\_add\_scalar()](reference-ed25519.md#ed25519_add_scalar())

[ed25519\_key\_exchange()](reference-ed25519.md#ed25519_key_exchange())

Alerts

[overview](reference-Alerts.md#overview)

[dht\_routing\_bucket](reference-Alerts.md#dht_routing_bucket)

[torrent\_alert](reference-Alerts.md#torrent_alert)

[peer\_alert](reference-Alerts.md#peer_alert)

[tracker\_alert](reference-Alerts.md#tracker_alert)

[torrent\_removed\_alert](reference-Alerts.md#torrent_removed_alert)

[read\_piece\_alert](reference-Alerts.md#read_piece_alert)

[file\_completed\_alert](reference-Alerts.md#file_completed_alert)

[file\_renamed\_alert](reference-Alerts.md#file_renamed_alert)

[file\_rename\_failed\_alert](reference-Alerts.md#file_rename_failed_alert)

[performance\_alert](reference-Alerts.md#performance_alert)

[state\_changed\_alert](reference-Alerts.md#state_changed_alert)

[tracker\_error\_alert](reference-Alerts.md#tracker_error_alert)

[tracker\_warning\_alert](reference-Alerts.md#tracker_warning_alert)

[scrape\_reply\_alert](reference-Alerts.md#scrape_reply_alert)

[scrape\_failed\_alert](reference-Alerts.md#scrape_failed_alert)

[tracker\_reply\_alert](reference-Alerts.md#tracker_reply_alert)

[dht\_reply\_alert](reference-Alerts.md#dht_reply_alert)

[tracker\_announce\_alert](reference-Alerts.md#tracker_announce_alert)

[hash\_failed\_alert](reference-Alerts.md#hash_failed_alert)

[peer\_ban\_alert](reference-Alerts.md#peer_ban_alert)

[peer\_unsnubbed\_alert](reference-Alerts.md#peer_unsnubbed_alert)

[peer\_snubbed\_alert](reference-Alerts.md#peer_snubbed_alert)

[peer\_error\_alert](reference-Alerts.md#peer_error_alert)

[peer\_connect\_alert](reference-Alerts.md#peer_connect_alert)

[peer\_disconnected\_alert](reference-Alerts.md#peer_disconnected_alert)

[invalid\_request\_alert](reference-Alerts.md#invalid_request_alert)

[torrent\_finished\_alert](reference-Alerts.md#torrent_finished_alert)

[piece\_finished\_alert](reference-Alerts.md#piece_finished_alert)

[request\_dropped\_alert](reference-Alerts.md#request_dropped_alert)

[block\_timeout\_alert](reference-Alerts.md#block_timeout_alert)

[block\_finished\_alert](reference-Alerts.md#block_finished_alert)

[block\_downloading\_alert](reference-Alerts.md#block_downloading_alert)

[unwanted\_block\_alert](reference-Alerts.md#unwanted_block_alert)

[storage\_moved\_alert](reference-Alerts.md#storage_moved_alert)

[storage\_moved\_failed\_alert](reference-Alerts.md#storage_moved_failed_alert)

[torrent\_deleted\_alert](reference-Alerts.md#torrent_deleted_alert)

[torrent\_delete\_failed\_alert](reference-Alerts.md#torrent_delete_failed_alert)

[save\_resume\_data\_alert](reference-Alerts.md#save_resume_data_alert)

[save\_resume\_data\_failed\_alert](reference-Alerts.md#save_resume_data_failed_alert)

[torrent\_paused\_alert](reference-Alerts.md#torrent_paused_alert)

[torrent\_resumed\_alert](reference-Alerts.md#torrent_resumed_alert)

[torrent\_checked\_alert](reference-Alerts.md#torrent_checked_alert)

[url\_seed\_alert](reference-Alerts.md#url_seed_alert)

[file\_error\_alert](reference-Alerts.md#file_error_alert)

[metadata\_failed\_alert](reference-Alerts.md#metadata_failed_alert)

[metadata\_received\_alert](reference-Alerts.md#metadata_received_alert)

[udp\_error\_alert](reference-Alerts.md#udp_error_alert)

[external\_ip\_alert](reference-Alerts.md#external_ip_alert)

[listen\_failed\_alert](reference-Alerts.md#listen_failed_alert)

[listen\_succeeded\_alert](reference-Alerts.md#listen_succeeded_alert)

[portmap\_error\_alert](reference-Alerts.md#portmap_error_alert)

[portmap\_alert](reference-Alerts.md#portmap_alert)

[portmap\_log\_alert](reference-Alerts.md#portmap_log_alert)

[fastresume\_rejected\_alert](reference-Alerts.md#fastresume_rejected_alert)

[peer\_blocked\_alert](reference-Alerts.md#peer_blocked_alert)

[dht\_announce\_alert](reference-Alerts.md#dht_announce_alert)

[dht\_get\_peers\_alert](reference-Alerts.md#dht_get_peers_alert)

[cache\_flushed\_alert](reference-Alerts.md#cache_flushed_alert)

[lsd\_peer\_alert](reference-Alerts.md#lsd_peer_alert)

[trackerid\_alert](reference-Alerts.md#trackerid_alert)

[dht\_bootstrap\_alert](reference-Alerts.md#dht_bootstrap_alert)

[torrent\_error\_alert](reference-Alerts.md#torrent_error_alert)

[torrent\_need\_cert\_alert](reference-Alerts.md#torrent_need_cert_alert)

[incoming\_connection\_alert](reference-Alerts.md#incoming_connection_alert)

[add\_torrent\_alert](reference-Alerts.md#add_torrent_alert)

[state\_update\_alert](reference-Alerts.md#state_update_alert)

[session\_stats\_alert](reference-Alerts.md#session_stats_alert)

[dht\_error\_alert](reference-Alerts.md#dht_error_alert)

[dht\_immutable\_item\_alert](reference-Alerts.md#dht_immutable_item_alert)

[dht\_mutable\_item\_alert](reference-Alerts.md#dht_mutable_item_alert)

[dht\_put\_alert](reference-Alerts.md#dht_put_alert)

[i2p\_alert](reference-Alerts.md#i2p_alert)

[dht\_outgoing\_get\_peers\_alert](reference-Alerts.md#dht_outgoing_get_peers_alert)

[log\_alert](reference-Alerts.md#log_alert)

[torrent\_log\_alert](reference-Alerts.md#torrent_log_alert)

[peer\_log\_alert](reference-Alerts.md#peer_log_alert)

[lsd\_error\_alert](reference-Alerts.md#lsd_error_alert)

[dht\_lookup](reference-Alerts.md#dht_lookup)

[dht\_stats\_alert](reference-Alerts.md#dht_stats_alert)

[incoming\_request\_alert](reference-Alerts.md#incoming_request_alert)

[dht\_log\_alert](reference-Alerts.md#dht_log_alert)

[dht\_pkt\_alert](reference-Alerts.md#dht_pkt_alert)

[dht\_get\_peers\_reply\_alert](reference-Alerts.md#dht_get_peers_reply_alert)

[dht\_direct\_response\_alert](reference-Alerts.md#dht_direct_response_alert)

[picker\_log\_alert](reference-Alerts.md#picker_log_alert)

[session\_error\_alert](reference-Alerts.md#session_error_alert)

[dht\_live\_nodes\_alert](reference-Alerts.md#dht_live_nodes_alert)

[session\_stats\_header\_alert](reference-Alerts.md#session_stats_header_alert)

[dht\_sample\_infohashes\_alert](reference-Alerts.md#dht_sample_infohashes_alert)

[block\_uploaded\_alert](reference-Alerts.md#block_uploaded_alert)

[alerts\_dropped\_alert](reference-Alerts.md#alerts_dropped_alert)

[socks5\_alert](reference-Alerts.md#socks5_alert)

[file\_prio\_alert](reference-Alerts.md#file_prio_alert)

[oversized\_file\_alert](reference-Alerts.md#oversized_file_alert)

[torrent\_conflict\_alert](reference-Alerts.md#torrent_conflict_alert)

[peer\_info\_alert](reference-Alerts.md#peer_info_alert)

[file\_progress\_alert](reference-Alerts.md#file_progress_alert)

[piece\_info\_alert](reference-Alerts.md#piece_info_alert)

[piece\_availability\_alert](reference-Alerts.md#piece_availability_alert)

[tracker\_list\_alert](reference-Alerts.md#tracker_list_alert)

[alert](reference-Alerts.md#alert)

[alert\_cast()](reference-Alerts.md#alert_cast())

[operation\_name()](reference-Alerts.md#operation_name())

[operation\_t](reference-Alerts.md#operation_t)

[int](reference-Core.md#int)

[alert\_category\_t](reference-Alerts.md#alert_category_t)
