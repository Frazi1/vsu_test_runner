import { ActiveDirectoryConnectionDataDto } from './ActiveDirectoryConnectionDataDto'

export class ActiveDirectorySearchRequestDto {
  connectionData: ActiveDirectoryConnectionDataDto
  baseSearch: string
  filterQuery: string
  userFieldToActiveDirectoryAttributeMapping: Map<string, string>


  constructor(connectionData: ActiveDirectoryConnectionDataDto                = new ActiveDirectoryConnectionDataDto(),
              baseSearch: string                                              = '',
              filterQuery: string                                             = '',
              userFieldToActiveDirectoryAttributeMapping: Map<string, string> = {}) {
    this.connectionData = connectionData
    this.baseSearch = baseSearch
    this.filterQuery = filterQuery
    this.userFieldToActiveDirectoryAttributeMapping = userFieldToActiveDirectoryAttributeMapping
  }
}
