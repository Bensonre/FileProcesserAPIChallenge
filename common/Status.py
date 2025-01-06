class Status:
    __PENDING = "PENDING"
    __QUEUED = "QUEUED"
    __PROCESSING = "PROCESSING"
    __PROCESSED = "PROCESSED"
    __DELIVERED = "DELIVERED"
    
    @staticmethod
    def get_status(value: int):
        match value:
            case 0:
                return Status.__PENDING
            case 1:
                return Status.__QUEUED
            case 2:
                return Status.__PROCESSING
            case 3:
                return Status.__PROCESSED
            case 4:
                return Status.__DELIVERED
            case _:
                return None