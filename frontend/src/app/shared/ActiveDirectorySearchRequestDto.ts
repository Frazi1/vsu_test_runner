import { ActiveDirectoryConnectionDataDto } from './ActiveDirectoryConnectionDataDto'

export class ActiveDirectorySearchRequestDto {
  connectionData: ActiveDirectoryConnectionDataDto
  baseSearch: string
  filterQuery: string
  userFieldToActiveDirectoryAttributeMapping: any


  constructor(connectionData: ActiveDirectoryConnectionDataDto = new ActiveDirectoryConnectionDataDto(),
              baseSearch: string                               = '',
              filterQuery: string                              = '',
              userFieldToActiveDirectoryAttributeMapping       = {}) {
    this.connectionData = connectionData
    this.baseSearch = baseSearch
    this.filterQuery = filterQuery
    this.userFieldToActiveDirectoryAttributeMapping = userFieldToActiveDirectoryAttributeMapping

    this.connectionData.host = 'ldap.forumsys.com'
    this.connectionData.port = 389
    this.connectionData.distinguishedName = 'cn=read-only-admin,dc=example,dc=com'
    this.connectionData.password = 'password'

    this.baseSearch = 'dc=example,dc=com'
    this.filterQuery = 'objectClass=person'
  }
}
