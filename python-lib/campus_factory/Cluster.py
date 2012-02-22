
import logging

from campus_factory.ClusterStatus import ClusterStatus
from campus_factory.OfflineAds.OfflineAds import OfflineAds

class Cluster:
    
    def __init__(self, cluster_unique, config, useOffline = False):
        self.cluster_unique = cluster_unique
        
        self.status = ClusterStatus(status_constraint="IsUndefined(Offline) && BOSCOCluster =?= \"%s\"" % self.cluster_unique)
        self.useOffline = useOffline
        if useOffline:
             self.offline = OfflineAds()
        self.config = config
        
    def ClusterMeetPreferences(self):
        idleslots = status.GetIdleGlideins()
        if idleslots == None:
            logging.info("Received None from idle glideins, going to try later")
            return False
        logging.debug("Idle glideins = %i" % idleslots)
        if idleslots >= int(self.config.get("general", "MAXIDLEGLIDEINS")):
            logging.info("Too many idle glideins")
            return False

        # Check for idle glidein jobs
        idlejobs = status.GetIdleGlideinJobs()
        if idlejobs == None:
            logging.info("Received None from idle glidein jobs, going to try later")
            return False
        logging.debug("Queued jobs = %i" % idlejobs)
        if idlejobs >= int(self.config.get("general", "maxqueuedjobs")):
            logging.info("Too many queued jobs")
            return False

        return True




    def GetIdleJobs(self):
        if not self.useOffline:
            return 0
        
        # Update the offline cluster information
        toSubmit = self.offline.Update( [self.cluster_unique] )
        
        # Get the delinquent sites
        num_submit = offline.GetDelinquentSites([self.cluster_unique])
        logging.debug("toSubmit from offline %s", str(toSubmit))
        logging.debug("num_submit = %s\n", str(num_submit))
            
        if (len(toSubmit) > 0) or num_submit[self.cluster_unique]:
            idleuserjobs = max([ num_submit[self.cluster_unique], 5 ])
            logging.debug("Offline ads detected jobs should be submitted.  Idle user jobs set to %i", idleuserjobs)
        else:
            logging.debug("Offline ads did not detect any matches or Delinquencies.")
            idleuserjobs = 0 
        
        return toSubmit
    
    
    
    
        
