# Project
- contract address (PK)
- name
- max supply
- metadata 
  - IPFS hash
  - API URL

# Token
- token ID (PK)
- contract address (FK)
- image
- token # (unique with contract)
- score
- rank
- trait value ID's (M2M)

# Trait Types
- trait type ID (PK)
- contract address (FK)
- trait type (unique with contract)

# Trait Value
- trait value ID (PK)
- trait type ID (FK)
- trait value (unique trait type ID)
- count
- score
- rarity
