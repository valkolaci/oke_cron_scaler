# -*- coding: UTF-8 -*-

import os
import sys
import yaml
import logging

# example config:
# schedules:
#   everyday:
#     - start: "0 20 5 * *"
#       end: "0 6 1 * *"
#       size: 0
#     - start: "0 20 1 * *"
#       end: "0 6 2 * *"
#       size: 0
#     - start: "0 20 2 * *"
#       end: "0 6 3 * *"
#       size: 0
#     - start: "0 20 3 * *"
#       end: "0 6 4 * *"
#       size: 0
#     - start: "0 20 4 * *"
#       end: "0 6 5 * *"
#       size: 0
#   weekend:
#     - start: "0 20 5 * *"
#       end: "0 6 1 * *"
#       size: 0
#   none: {}
# rules:
#   - compartment: sandbox/devops
#     schedule: everyday
#   - compartment: enap/cmp-tst
#     schedule: everyday
#   - compartment: enap/cmp-uat
#     schedule: weekend
#   - compartment: enap/cmp-prod
#     schedule: none
# exceptions:
#   - comment: Weekend testing
#     compartment: sandbox/devops
#     startdate: 2025-12-19
#     starttime: 18:00
#     enddate: 2025-12-22
#     endtime: 06:00
#     size: on
#   - comment: Holiday
#     startdate: 2025-12-24
#     starttime: 00:00
#     enddate: 2025-12-28
#     endtime: 00:00
#     size: 0

class Config:
  DEFAULT_CONFIG_FILE = "rules.yaml"

  config = None

# initialize global config instance
  def read_config():
    Config.config = Config()

# read config file and init object
  def __init__(self):
    try:
      config_filename = os.getenv('CONFIG_FILE', Config.DEFAULT_CONFIG_FILE)
      
      logging.info('Reading config file %s' % (config_filename))
      stream = open(config_filename, 'r')
      self.config = yaml.safe_load(stream)
      self.contents = self.process_config_contents()
    except Exception as e:
      fatal_exception('during loading config file', e)

# process config contents
  def process_config_contents(self):
    contents = self.check_config_option_string('listen.bearer_token', default='', emptyDefault=True)
    contents = dict()
    return contents

# check config option
  def check_config_option(self, name, default=None, skipEmpty=False):
    name_components = name.split('.')
    env_name = '_'.join(name_components).upper()
    value = os.getenv(env_name)
    if value is not None:
      if value != '':
        return value
      if not skipEmpty:
        return value
    ptr = self.config
    found = True
    for component in name_components:
      if not isinstance(ptr, dict):
        found = False
        break
      if not component in ptr:
        found = False
        break
      ptr = ptr[component]
    if found:
      return ptr
    return default

# check string config option
  def check_config_option_string(self, name, minLen=-1, maxLen=-1, default=None, emptyDefault=False, skipEmpty=False):
    value = self.check_config_option(name, default, skipEmpty=skipEmpty)
    if value is None:
      if minLen > 0:
        logging.error('Invalid config option %s: missing but mandatory' % (name))
        sys.exit(1)
      return value
    if isinstance(value, list):
      logging.error('Invalid config option %s type: list' % (name))
      sys.exit(1)
    if isinstance(value, dict):
      logging.error('Invalid config option %s type: dict' % (name))
      sys.exit(1)
    value = str(value)
    length = len(value)
    if value == '' and emptyDefault:
      return default
    if minLen >= 0 and length < minLen:
      logging.error('Invalid config option %s: \'%s\' is shorter than minimum %d' % (name, value, minLen))
      sys.exit(1)
    if maxLen >= 0 and length > maxLen:
      logging.error('Invalid config option %s: \'%s\' is longer than maximum %d' % (name, value, maxLen))
      sys.exit(1)
    return value

# check list or string config option
  def check_config_option_list_or_string(self, name, minNum=-1, maxNum=-1, default=None, skipEmpty=False):
    value = self.check_config_option(name, default, skipEmpty=skipEmpty)
    if value is None:
      if minNum > 0:
        logging.error('Invalid config option %s: missing but mandatory' % (name))
        sys.exit(1)
    if isinstance(value, dict):
      logging.error('Invalid config option %s type: dict' % (name))
      sys.exit(1)
    if isinstance(value, list):
      listvalue = value
      retlist = []
      if len(listvalue) < 1 and emptyDefault:
        return default
      for value in listvalue:
        if isinstance(value, list):
          logging.error('Invalid config option %s list entry type: list' % (name))
          sys.exit(1)
        if isinstance(value, dict):
          logging.error('Invalid config option %s list entry type: dict' % (name))
          sys.exit(1)
        value = str(value)
        retlist.append(value)
      if minNum > 0 and minNum > len(retlist):
        logging.error('Invalid config option %s: list length %d is less than %d values expected' % (name, len(retlist), minNum))
        sys.exit(1)
      if maxNum > 0 and maxNum < len(retlist):
        logging.error('Invalid config option %s: list length %d is more than %d values allowed' % (name, len(retlist), maxNum))
        sys.exit(1)
      return retlist
    value = str(value)
    length = len(value)
    if value == '' and emptyDefault:
      return default
    if minNum > 1:
      logging.error('Invalid config option %s: a single value \'%s\' is less than %d values expected' % (name, value, minNum))
      sys.exit(1)
    return [value]

# check dict config option
  def check_config_option_dict(self, name, minNum=-1, maxNum=-1, default=None, skipEmpty=False):
    value = self.check_config_option(name, default, skipEmpty=skipEmpty)
    if value is None:
      if minNum > 0:
        logging.error('Invalid config option %s: missing but mandatory' % (name))
        sys.exit(1)
    if not isinstance(value, dict):
      logging.error('Invalid config option %s type: not a dict' % (name))
      sys.exit(1)
    dictvalue = value
    retdict = {}
    if len(dictvalue) < 1 and emptyDefault:
      return default
    for key, value in dictvalue.items():
      if isinstance(value, list):
        logging.error('Invalid config option %s dict entry type: list' % (name))
        sys.exit(1)
      if isinstance(value, dict):
        logging.error('Invalid config option %s dict entry type: dict' % (name))
        sys.exit(1)
      value = str(value)
      retdict[key] = value
    if minNum > 0 and minNum > len(retdict):
      logging.error('Invalid config option %s: dict size %d is less than %d values expected' % (name, len(retdict), minNum))
      sys.exit(1)
    if maxNum > 0 and maxNum < len(retdict):
      logging.error('Invalid config option %s: dict size %d is more than %d values allowed' % (name, len(retdict), maxNum))
      sys.exit(1)
    return retdict
