import copy

import mock
import pytest

from swimlane.core.resources.record import Record, record_factory
from swimlane.exceptions import UnknownField, ValidationError


class TestRecord(object):
    def test_repr(self, mock_record):
        assert repr(mock_record) == '<Record: RA-7>'
        assert repr(record_factory(mock_record.app)) == '<Record: RA - New>'

    def test_save(self, mock_swimlane, mock_record):
        """Test save endpoint called with correct args"""

        with mock.patch.object(mock_swimlane, 'request') as mock_request:
            with mock.patch.object(mock_record, 'validate') as mock_validate:

                mock_request.return_value.json.return_value = mock_record._raw

                mock_record['Numeric'] = 5
                mock_record.save()

                mock_validate.assert_called_once_with()
                mock_request.assert_called_once_with(
                    'put',
                    'app/{}/record'.format(mock_record.app.id),
                    json={'$type': 'Core.Models.Record.Record, Core', 'actionsExecuted': {'$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Object, mscorlib]], mscorlib'}, 'allowed': [], 'applicationId': '58e4bb4407637a0e4c4f9873', 'applicationRevision': 0.0, 'comments': {'$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Collections.Generic.List`1[[Core.Models.Record.Comments, Core]], mscorlib]], mscorlib', 'a3uau': [{'$type': 'Core.Models.Record.Comments, Core', 'createdByUser': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core', 'id': '58de1d1c07637a0264c0ca6a', 'name': 'admin'}, 'createdDate': '2017-04-19T18:40:25.529Z', 'message': 'Example comment'}]}, 'createdDate': '0001-01-01T00:00:00', 'disabled': False, 'id': '58ebb22807637a02d4a14bd6', 'isNew': False, 'linkedData': {'$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Object, mscorlib]], mscorlib'}, 'modifiedDate': '0001-01-01T00:00:00', 'referencedByIds': [], 'referencedRecordIds': [], 'sessionTimeSpent': 0, 'timeTrackingEnabled': True, 'totalTimeSpent': 0, 'trackingId': 7.0, 'values': {'$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Object, mscorlib]], mscorlib', '58e4bb4407637a0e4c4f9875': 'RA-7', 'a04rv': '10.0.1.184:56005:3172', 'a0g40': 'Alert Action', 'a0k7v': {'$type': 'Core.Models.Record.ValueSelection, Core', 'id': '58e7bae8c61082e377cc4d82', 'value': 'Open'}, 'a11mn': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core', 'id': '58de1d1c07637a0264c0ca6a', 'name': 'admin'}, 'a18qr': 'User.Activity.Failed Logins', 'a1k2a': 'https://app.threatconnect.com/auth/threat/threat.xhtml?threat=2058283', 'a1r3v': 'Logon', 'a2gor': 'Transparent Tribe', 'a2ybt': 'Germany', 'a365t': '2017-04-05T13:00:00.000000Z', 'a3rvw': '3172', 'a3w8f': ['58e24e8607637a0b488849c0', '58e24e8607637a0b488849ca', '58e24dc507637a0b48884950'], 'a44wz': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core', 'id': '58de1d1c07637a0264c0ca71', 'name': 'Everyone'}, 'a4l9p': 'logdec1', 'a5g30': 'C2', 'a5v09': {'$type': 'Core.Models.Record.ValueSelection, Core', 'id': '58e7bafd83f418637cf91c3e', 'value': 'ESA Alert'}, 'a5yg3': '3172', 'a6if8': '[{"lifetime": "60", "rid": "4531291", "payload": "7808", "size": "11956", "service": "0", "eth.src": "00:0C:29:5B:98:5E", "feed.name": "Swimlane_Feed", "medium": "1", "ip.dst": "178.238.235.143", "org.dst": "Contabo GmbH", "sessionid": "4534669", "latdec.dst": "51.2993", "eth.type": "2048", "ip.src": "10.0.1.183", "domain.dst": "contabo.host", "eth.dst": "00:50:56:A7:4D:79", "did": "packdec1", "longdec.dst": "9.491", "packets": "122", "streams": "2", "country.dst": "Germany", "time": 1491593904, "ip.proto": "1"}]', 'a7bgv': '2017-04-21T00:00:00.000000Z', 'a7gm5': '<14>Apr  5 23:42:54 localhost CEF:0|RSA|Security Analytics ESA|10.4|Module_58e40ea9e4b070dfd2a59ad5_Alert|Alert Action|7|rt=2017-04-05T23:42Z id=890eb2b1-2d90-46a5-b1ed-6e58b408ed83 source=10.0.1.184:56005:3172  action=authentication failure;; client=sshd;; device_class=Unix;; device_ip=10.0.1.178;; device_type=crossbeamc;; did=logdec1;; ec_activity=Logon;; ec_outcome=Failure;; ec_subject=User;; ec_theme=Authentication;; esa_time=1491435774280;; event_cat_name=User.Activity.Failed Logins;; event_source_id=10.0.1.184:56005:3172;; header_id=0006;; host_src=178.238.235.143;; level=4;; medium=32;; msg_id=000103;; rid=3172;; sessionid=3172;; size=175;; time=1491435771;; user_dst=user;; username=0;;\x00', 'a7ira': 'User', 'a8vjm': 'Failure', 'a990o': '7', 'aabxm': 'Threat', 'aag0z': '<table class="table table-bordered table-hover"><tr><th>lifetime</th><th>rid</th><th>payload</th><th>size</th><th>service</th><th>eth.src</th><th>country.dst</th><th>medium</th><th>ip.dst</th><th>org.dst</th><th>sessionid</th><th>latdec.dst</th><th>eth.type</th><th>ip.src</th><th>domain.dst</th><th>eth.dst</th><th>did</th><th>longdec.dst</th><th>packets</th><th>streams</th><th>feed.name</th><th>time</th><th>ip.proto</th></tr><tr><td>60</td><td>4531291</td><td>7808</td><td>11956</td><td>0</td><td>00:0C:29:5B:98:5E</td><td>Germany</td><td>1</td><td>178.238.235.143</td><td>Contabo GmbH</td><td>4534669</td><td>51.2993</td><td>2048</td><td>10.0.1.183</td><td>contabo.host</td><td>00:50:56:A7:4D:79</td><td>packdec1</td><td>9.491</td><td>122</td><td>2</td><td>Swimlane_Feed</td><td>1491593904</td><td>1</td></tr></table>', 'aasnf': {'$type': 'Core.Models.Record.ValueSelection, Core', 'id': '58e7bb144121bd73d8f53845', 'value': 'High'}, 'aazhn': 'MYTHICLEOPARD', 'ac1oa': '2017-04-02T23:42:00.000000Z', 'acl9o': 'Mar 29 08:59:50 splunk lxcfs[940]:   4: fd:   9: net_cls,net_prio\nMar 29 08:59:50 splunk kernel: [    0.000000] Hypervisor detected: VMware\nMar 29 08:59:50 splunk kernel: [    0.000000] NODE_DATA(0) allocated [mem 0x13fff8000-0x13fffcfff]\nMar 29 08:59:50 splunk kernel: [    0.000000] RCU: Adjusting geometry for rcu_fanout_leaf=64, nr_cpu_ids=4\nMar 29 08:59:50 splunk kernel: [    0.000000] console [tty0] enabled\nMar 29 08:59:50 splunk kernel: [    0.187011] PM: Registering ACPI NVS region [mem 0xbfeff000-0xbfefffff] (4096 bytes)\nMar 29 08:59:50 splunk kernel: [    0.289673] pci 0000:00:15.4: [15ad:07a0] type 01 class 0x060400\nMar 29 08:59:50 splunk kernel: [    0.306003] pci 0000:00:18.5: System wakeup disabled by ACPI\nMar 29 08:59:50 splunk kernel: [    0.317367] pci 0000:00:15.4: PCI bridge to [bus 07]\nMar 29 08:59:50 splunk kernel: [    0.324226] pci 0000:00:18.3: PCI bridge to [bus 1e]\nMar 29 08:59:50 splunk kernel: [    0.374053] pci 0000:00:17.6: bridge window [io  0x1000-0x0fff] to [bus 19] add_size 1000\nMar 29 08:59:50 splunk kernel: [    0.376241] pci 0000:00:17.5: BAR 13: failed to assign [io  size 0x1000]\nMar 29 08:59:50 splunk kernel: [    0.381821] pci 0000:00:15.3: PCI bridge to [bus 06]\nMar 29 08:59:50 splunk kernel: [    0.389813] pci 0000:00:18.2: PCI bridge to [bus 1d]\nMar 29 08:59:50 splunk kernel: [    0.391570] pci_bus 0000:13: resource 2 [mem 0xeb800000-0xeb8fffff 64bit pref]\nMar 29 08:59:50 splunk kernel: [    0.788759] pcie_pme 0000:00:15.0:pcie01: service driver pcie_pme loaded\nMar 29 08:59:50 splunk kernel: [    0.796112] pciehp 0000:00:15.6:pcie04: service driver pciehp loaded\nMar 29 08:59:50 splunk kernel: [    0.852911] ehci-pci: EHCI PCI platform driver\nMar 29 08:59:50 splunk kernel: [    2.111909] AVX version of gcm_enc/dec engaged.\nMar 29 08:59:50 splunk kernel: [    4.099053] md: raid4 personality registered for level 4\nMar 29 08:59:50 splunk irqbalance[1106]:    ...done.\nMar 29 11:12:59 splunk sshd[3125]: fatal: Unable to negotiate with 10.0.1.10 port 55450: no matching key exchange method found. Their offer: diffie-hellman-group1-sha1 [preauth]\nMar 29 19:56:21 splunk sshd[9399]: fatal: Unable to negotiate with 10.0.1.10 port 50808: no matching key exchange method found. Their offer: diffie-hellman-group1-sha1 [preauth]\nMar 30 05:17:01 splunk CRON[16176]: pam_unix(cron:session): session opened for user root by (uid=0)\nMar 30 13:16:22 splunk systemd[1]: apt-daily.timer: Adding 1h 12min 7.795190s random time.\nMar 30 18:22:08 splunk sshd[26877]: fatal: Unable to negotiate with 10.0.1.10 port 47092: no matching key exchange method found. Their offer: diffie-hellman-group1-sha1 [preauth]\nMar 31 03:17:01 splunk CRON[1496]: pam_unix(cron:session): session closed for user root\nMar 31 11:17:01 splunk CRON[7743]: pam_unix(cron:session): session closed for user root\nMar 31 19:36:54 splunk systemd[1]: apt-daily.timer: Adding 3h 28min 17.687266s random time.\nMar 31 20:17:01 splunk CRON[14688]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)\nApr  1 05:43:20 splunk systemd[1]: snapd.refresh.timer: Adding 3h 41min 31.130550s random time.\nApr  1 13:17:01 splunk CRON[27787]: pam_unix(cron:session): session opened for user root by (uid=0)\nApr  1 23:08:55 splunk sshd[2991]: fatal: Unable to negotiate with 10.0.1.10 port 45758: no matching key exchange method found. Their offer: diffie-hellman-group1-sha1 [preauth]\nApr  2 06:47:01 splunk CRON[9119]: pam_unix(cron:session): session opened for user root by (uid=0)\nApr  2 06:47:03 splunk CRON[9119]: pam_unix(cron:session): session closed for user root\nApr  2 15:26:13 splunk sshd[15787]: fatal: Unable to negotiate with 10.0.1.10 port 51872: no matching key exchange method found. Their offer: diffie-hellman-group1-sha1 [preauth]\nApr  3 00:17:01 splunk CRON[22704]: pam_unix(cron:session): session opened for user root by (uid=0)\nApr  3 08:58:35 splunk sshd[29536]: fatal: Unable to negotiate with 10.0.1.10 port 44038: no matching key exchange method found. Their offer: diffie-hellman-group1-sha1 [preauth]\nApr  3 18:17:01 splunk CRON[4260]: pam_unix(cron:session): session closed for user root\nApr  4 10:17:01 splunk CRON[15857]: pam_unix(cron:session): session opened for user root by (uid=0)\nApr  4 15:01:51 splunk sshd[19167]: pam_unix(sshd:auth): check pass; user unknown\nApr  4 15:12:20 splunk sshd[19342]: Failed password for invalid user admin from 10.0.3.200 port 61969 ssh2\nApr  4 15:23:20 splunk sshd[19546]: PAM 1 more authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=10.0.3.200\nApr  4 15:45:18 splunk sshd[19814]: pam_unix(sshd:auth): check pass; user unknown\nApr  4 16:08:34 splunk sshd[20033]: Invalid user admin from 10.0.3.200\nApr  4 22:17:01 splunk CRON[24590]: pam_unix(cron:session): session opened for user root by (uid=0)\nApr  5 11:17:01 splunk CRON[1667]: pam_unix(cron:session): session opened for user root by (uid=0)\nApr  5 11:17:01 splunk CRON[1667]: pam_unix(cron:session): session closed for user root\nApr  5 13:21:41 splunk sshd[3382]: message repeated 2 times: [ Failed password for user from 10.0.3.200 port 61496 ssh2]\nApr  5 13:35:07 splunk systemd-logind[996]: New session 202 of user user.\nApr  5 17:16:14 splunk systemd[1]: snapd.refresh.timer: Adding 3h 48min 41.276237s random time.\nApr  6 09:17:01 splunk CRON[18136]: pam_unix(cron:session): session closed for user root\nApr  6 09:17:10 splunk systemd[1]: Started Cleanup of Temporary Directories.\nApr  7 00:17:01 splunk CRON[29019]: pam_unix(cron:session): session closed for user root\nApr  7 11:17:01 splunk CRON[4922]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)\nApr  7 16:45:09 splunk sshd[9179]: Connection closed by 10.0.1.10 port 44167 [preauth]\nApr  7 22:40:33 splunk sshd[13666]: fatal: Unable to negotiate with 10.0.1.10 port 60949: no matching host key type found. Their offer: ecdsa-sha2-nistp521 [preauth]\nApr  7 23:17:01 splunk CRON[14063]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)\nApr  8 05:42:16 splunk sshd[19026]: Did not receive identification string from 10.0.1.10\nApr  8 10:48:13 splunk systemd[1]: snapd.refresh.timer: Adding 4h 27min 21.903828s random time.\nApr  8 17:17:01 splunk CRON[27791]: pam_unix(cron:session): session closed for user root\nApr  8 23:32:33 splunk sshd[32530]: Connection closed by 10.0.1.10 port 48600 [preauth]\nApr  8 23:32:33 splunk sshd[32533]: fatal: Unable to negotiate with 10.0.1.10 port 48615: no matching host key type found. Their offer: ecdsa-sha2-nistp384 [preauth]\nApr  9 05:25:42 splunk sshd[4731]: fatal: Unable to negotiate with 10.0.1.10 port 46071: no matching host key type found. Their offer: ecdsa-sha2-nistp384 [preauth]\nApr  9 11:22:54 splunk sshd[9292]: Protocol major versions differ for 10.0.1.10: SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.1 vs. SSH-1.5-Nmap-SSH1-Hostkey\nApr  9 17:18:35 splunk sshd[13798]: Protocol major versions differ for 10.0.1.10: SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.1 vs. SSH-1.5-NmapNSE_1.0\nApr  9 23:17:01 splunk CRON[18223]: pam_unix(cron:session): session closed for user root\nApr 10 02:17:01 splunk CRON[20422]: pam_unix(cron:session): session closed for user root\nApr 10 04:17:01 splunk CRON[22016]: pam_unix(cron:session): session closed for user root\nApr 10 06:32:03 splunk sshd[23779]: fatal: Unable to negotiate with 10.0.1.10 port 51063: no matching host key type found. Their offer: ecdsa-sha2-nistp521 [preauth]\nApr 10 09:18:01 splunk systemd[1]: Starting Cleanup of Temporary Directories...\nApr 10 09:18:01 splunk systemd[1]: Started Cleanup of Temporary Directories.\n', 'acqdq': '1491435774280', 'aep2e': [{'$type': 'Core.Models.Record.Attachment, Core', 'fileId': '58ebb22907637a0b488b7b17', 'filename': '5f09afe50064b2bd718e77818b565df1.pcap', 'uploadDate': '2017-04-10T16:26:17.017Z'}], 'af967': '890eb2b1-2d90-46a5-b1ed-6e58b408ed83', 'afbbv': '', 'afff3': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core', 'id': '58de1d1c07637a0264c0ca6a', 'name': 'admin'}, 'afrn3': 'ThreatType/Targeted, KillChain/C2, MaliciousConfidence/High, Actor/MYTHICLEOPARD', 'agn03': [{'$type': 'Core.Models.Utilities.UserGroupSelection, Core', 'id': '58de1d1c07637a0264c0ca6a', 'name': 'admin'}, {'$type': 'Core.Models.Utilities.UserGroupSelection, Core', 'id': '58ebc11107637a02d4a23f14', 'name': 'wade wilson'}], 'agoat': [{'$type': 'Core.Models.Record.Attachment, Core', 'fileId': '58ebb22a07637a0b488b7db3', 'filename': '362a36190a149866cf0f54e0fd119338.log', 'uploadDate': '2017-04-10T16:26:18.548Z'}], 'ah7js': 'high', 'ahdtf': 'http://mail.vdjunky.org/, http://www.vdjunky.org/, http://vdjunky.org/, http://178.238.235.143:9001/, http://178.238.235.143/, http://m1343.contabo.host/', 'ahep6': 'TLP RED', 'ahziu': '178.238.235.143', 'aiir8': '2017-04-10T16:26:16.389000Z', 'aio1w': 'sshd', 'akxvh': 177360000, 'alnet': 'ip_address', 'amjd0': 'ns1.contabo.net,ns2.contabo.net', 'anet4': '10.0.1.183, 178.238.235.143', 'ao64i': '2017-04-21T21:00:10.942000Z', 'aokp5': 'Unix', 'apf9i': '10.0.1.178', 'aqc6k': 'Contabo GmbH', 'aqkg3': 5, 'arlrt': [{'$type': 'Core.Models.Record.ValueSelection, Core', 'id': '58fae4eafef0eead26dee65c', 'value': 'Option 2'}, {'$type': 'Core.Models.Record.ValueSelection, Core', 'id': '58fae4c59173122945a7cff6', 'value': 'Option 1'}], 'arnd6': 'authentication failure', 'arok4': 'crossbeamc', 'au7ic': 'vdjunky.org, a6f8b4b528d67fe5b985ad0a394e46f5c116bb80b7cb8ca9a094d92f4dc614c1, 9b98abb9a9fa714e05d43b08b76c0afa, 85429d5f2745d813e53b28d3d953d1cd, 3e91836b89b6d6249741dc8ee0d2895a, tcp.vdjunky.org, 8253dd13c126c44483bcbde23e61d53d', 'aw9gd': 'ip.src=10.0.1.178 || ip.dst=10.0.1.178', 'awmtq': 'Authentication', 'axdvr': '175', 'ayqk6': '178.238.235.143', 'azfys': 2058283, 'azygs': {'$type': 'Core.Models.Utilities.UserGroupSelection, Core', 'id': '58de1d1c07637a0264c0ca71', 'name': 'Everyone'}}, 'visualizations': {'$type': 'System.Collections.Generic.Dictionary`2[[System.String, mscorlib],[System.Collections.Generic.List`1[[Core.Models.Record.VisualizationData, Core]], mscorlib]], mscorlib'}})

                # Test validation failure
                mock_validate.side_effect = ValidationError(mock_record, 'Test error')

                with pytest.raises(ValidationError):
                    mock_record.save()

                assert mock_validate.call_count == 2
                assert mock_request.call_count == 1

    def test_delete(self, mock_swimlane, mock_record):
        """Test record can be deleted when not new and that deleted records lose their ID but maintain their fields"""
        with mock.patch.object(mock_swimlane, 'request') as mock_request:
            with mock.patch.object(mock_record, 'validate') as mock_validate:

                mock_record['Numeric'] = 5
                rec_id = mock_record.id

                mock_record.delete()
                mock_request.assert_called_once_with(
                    'delete',
                    'app/{}/record/{}'.format(mock_record.app.id, rec_id)
                )

                assert mock_record.id is None
                assert mock_record['Numeric'] == 5

                with pytest.raises(ValueError):
                    mock_record.delete()

    def test_validate_required_fields(self, mock_record):
        """Test validate method checks for required fields"""
        assert mock_record.validate() is None

        field_name = 'Numeric'
        mock_record[field_name] = None
        mock_record._fields[field_name].required = True

        with pytest.raises(ValidationError):
            mock_record.validate()

    def test_ordering(self, mock_record, mock_app):
        record_copy = Record(mock_record.app, mock_record._raw)

        # Equality by id and app id
        assert record_copy == mock_record

        record_copy.id = '58ebb22807637a02d4a14bd7'

        assert record_copy != mock_record

        # Ordering by tracking id and app name
        record_copy.tracking_id = 'RA-16'
        assert mock_record < record_copy

        # Verify can't sort/order against non-record instances
        with pytest.raises(TypeError):
            mock_record < mock_app

    def test_incorrect_app_id_failure(self, mock_app):
        """Test that retrieving a record validates source app has expected application ID"""
        with pytest.raises(ValueError):
            Record(mock_app, {
                '$type': Record._type,
                'isNew': False,
                'applicationId': mock_app.id + '1234',
            })

    def test_unknown_field_access(self, mock_record):
        """Test accessing a missing field raises UnknownField"""

        # Get
        try:
            mock_record['Muneric']
        except UnknownField as error:
            assert error.field_name == 'Muneric'
            assert error.similar_field_names == ['Numeric']
            assert error.app is mock_record.app
        else:
            raise RuntimeError

        # Set
        try:
            mock_record['Muneric'] = 5
        except UnknownField as error:
            assert error.field_name == 'Muneric'
            assert error.similar_field_names == ['Numeric']
            assert error.app is mock_record.app
        else:
            raise RuntimeError

    def test_iteration(self, mock_record):
        """Test that iterating over a record yields field names and their values like dict.items()"""
        num_fields = 0

        for field_name, field_value in mock_record:
            num_fields += 1
            assert field_value == mock_record[field_name]

        assert num_fields > 0

    def test_add_restriction(self, mock_swimlane, random_mock_user, mock_record):
        """Test adding usergroup restrictions to a record"""

        with pytest.raises(TypeError):
            mock_record.add_restriction()

        with pytest.raises(TypeError):
            mock_record.add_restriction(object())

        assert len(mock_record._raw['allowed']) == 0
        assert len(mock_record.restrictions) == 0

        mock_record.add_restriction(mock_swimlane.user)
        assert mock_swimlane.user in mock_record.restrictions
        assert len(mock_record._raw['allowed']) == 1

        mock_record.add_restriction(mock_swimlane.user)
        assert len(mock_record.restrictions) == 1

        mock_record.add_restriction(random_mock_user)
        assert len(mock_record.restrictions) == 2


    def test_remove_restriction(self, mock_swimlane, random_mock_user, mock_record):
        """Test adding usergroup restrictions to a record"""

        assert len(mock_record.restrictions) == 0
        mock_record.add_restriction(mock_swimlane.user, random_mock_user)

        with pytest.raises(TypeError):
            mock_record.remove_restriction(object())

        mock_record.remove_restriction()
        assert len(mock_record.restrictions) == 0

        with pytest.raises(ValueError):
            mock_record.remove_restriction(mock_swimlane.user)

        mock_record.add_restriction(mock_swimlane.user, random_mock_user)

        mock_record.remove_restriction(mock_swimlane.user)

        assert random_mock_user in mock_record.restrictions

    def test_ignore_caching_when_unsaved(self, mock_record):
        """Test cache index keys are only returned when record has id, disabling caching when unsaved"""

        assert mock_record.get_cache_index_keys()

        mock_record.id = None
        with pytest.raises(NotImplementedError):
            mock_record.get_cache_index_keys()

    def test_record_field_resolvable_by_key(self, mock_record):
        """Test that fields can be resolved by their keys"""
        assert mock_record.get_field('Action') is mock_record.get_field('action-key')

    def test_record_keys_not_included_in_field_names(self, mock_record):
        """Make sure fields keys don't show up when iterating a record"""
        assert 'action-key' not in dict(mock_record)
