from kafka import KafkaConsumer
import json
import pickle

# Load the trained model
with open('network_model.pk3', 'rb') as m:
    model = pickle.load(m)

# Setting up the Kafka consumer to listen to the 'test-data' topic
consumer = KafkaConsumer(
    'test-data',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# feature order expected  by the model we trained
feature_order = [ 'proto_3pc', 'proto_a/n', 'proto_aes-sp3-d', 'proto_any', 'proto_argus', 'proto_aris', 'proto_arp', 
'proto_ax.25', 'proto_bbn-rcc', 'proto_bna', 'proto_br-sat-mon', 'proto_cbt', 'proto_cftp', 
'proto_chaos', 'proto_compaq-peer', 'proto_cphb', 'proto_cpnx', 'proto_crtp', 'proto_crudp', 
'proto_dcn', 'proto_ddp', 'proto_ddx', 'proto_dgp', 'proto_egp', 'proto_eigrp', 'proto_emcon', 
'proto_encap', 'proto_etherip', 'proto_fc', 'proto_fire', 'proto_ggp', 'proto_gmtp', 'proto_gre', 
'proto_hmp', 'proto_i-nlsp', 'proto_iatp', 'proto_ib', 'proto_icmp', 'proto_idpr', 'proto_idpr-cmtp', 
'proto_idrp', 'proto_ifmp', 'proto_igmp', 'proto_igp', 'proto_il', 'proto_ip', 'proto_ipcomp', 
'proto_ipcv', 'proto_ipip', 'proto_iplt', 'proto_ipnip', 'proto_ippc', 'proto_ipv6', 'proto_ipv6-frag', 
'proto_ipv6-no', 'proto_ipv6-opts', 'proto_ipv6-route', 'proto_ipx-n-ip', 'proto_irtp', 'proto_isis', 
'proto_iso-ip', 'proto_iso-tp4', 'proto_kryptolan', 'proto_l2tp', 'proto_larp', 'proto_leaf-1', 
'proto_leaf-2', 'proto_merit-inp', 'proto_mfe-nsp', 'proto_mhrp', 'proto_micp', 'proto_mobile', 
'proto_mtp', 'proto_mux', 'proto_narp', 'proto_netblt', 'proto_nsfnet-igp', 'proto_nvp', 'proto_ospf', 
'proto_pgm', 'proto_pim', 'proto_pipe', 'proto_pnni', 'proto_pri-enc', 'proto_prm', 'proto_ptp', 
'proto_pup', 'proto_pvp', 'proto_qnx', 'proto_rdp', 'proto_rsvp', 'proto_rtp', 'proto_rvd', 
'proto_sat-expak', 'proto_sat-mon', 'proto_sccopmce', 'proto_scps', 'proto_sctp', 'proto_sdrp', 
'proto_secure-vmtp', 'proto_sep', 'proto_skip', 'proto_sm', 'proto_smp', 'proto_snp', 
'proto_sprite-rpc', 'proto_sps', 'proto_srp', 'proto_st2', 'proto_stp', 'proto_sun-nd', 
'proto_swipe', 'proto_tcf', 'proto_tcp', 'proto_tlsp', 'proto_tp++', 'proto_trunk-1', 
'proto_trunk-2', 'proto_ttp', 'proto_udp', 'proto_unas', 'proto_uti', 'proto_vines', 
'proto_visa', 'proto_vmtp', 'proto_vrrp', 'proto_wb-expak', 'proto_wb-mon', 'proto_wsn', 
'proto_xnet', 'proto_xns-idp', 'proto_xtp', 'proto_zero', 'service_-', 'service_dhcp', 
'service_dns', 'service_ftp', 'service_ftp-data', 'service_http', 'service_irc', 'service_pop3', 
'service_radius', 'service_smtp', 'service_snmp', 'service_ssh', 'service_ssl', 'state_CON', 
'state_ECO', 'state_FIN', 'state_INT', 'state_PAR', 'state_REQ', 'state_RST', 'state_URN', 'state_no']


message_count = 0

try:
    print("Waiting for messages...")
    for message in consumer:
        data = message.value
        print(f"Received message: {data}")

        if all(feature in data for feature in feature_order):
            features = [data[feature] for feature in feature_order]
            print(f"Extracted features: {features}")

            # Predict test input using the model
            prediction = model.predict([features])
            print(f"AI Prediction Result: {prediction}")
        else:
            print("Missing features in the message")


        message_count += 1
        if message_count >= 100:  # limit
            break

except Exception as e:
    print(f"Error occurred: {e}")
