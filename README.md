# Knowledge Graph Enabled Search Accelerator

This repo contains the core components for the Knowledge Graph Enabled Search solution.
The solution is designed as a template such that you can reuse the basic structure of the solution by overwriting its individual components based on the requirement of your application. 
For example, you can ingest your own knowledge graph and implement your own query rewriting logic that tailored to your application.

The solution can be generalized to different kind of industries. In this template, we use a sample knowledge graph and documents from medical domain to demonstrate the end-2-end solution. 

# Why introducing knowledge graph to search engine

For general search engine like Lucene, Azure Cognitive Search, etc., they index the documents by terms and rank the results based on term frequency. These search engines, however, are not designed to interpret the complex mental associations humans natually create between various concepts. 

Here is an example by [Uber Eat](https://eng.uber.com/uber-eats-query-understanding/): an eater might have a certain type of food in mind, but choose something else while browsing the app. For example, an eater might search for udon, but end up ordering soba. In this case, the eater may have been looking for something similar to udon, such as soba and ramen, instead of only being interested in udon. As humans, it might seem obvious; Udon and soba are somewhat similar, Chinese and Japanese are both Asian cuisines. However, machines have a more difficult time understanding these similarities only based on the textual information. In fact, a lot of work goes into training them to make these types of intelligent decisions on the semantic level. 

Uber's solution is to first build a food knowledge graph. Then, based the knowledge graph, it will try to interpret the intent behind user's search. In the above example, the knowledge graph will tell us that udon is similar to ramen and soba, and it is a kind of Japanse food. So, besides of searching "udon", it will also search for "ramen", "soda" and other "Japanese" food. This can provide more options to the user that better meet his/her intention. Expecially, it will be very useful when there is no restaurant nearby is selling "udon".    

<figure>
<img src="http://1fykyq3mdn5r21tpna3wkdyi-wpengine.netdna-ssl.com/wp-content/uploads/2018/06/Figure_3.jpg" alt="Trulli" class="center" style="width:50%">
<figcaption align = "center"><b>Fig.1 - Food Knowledge Graph</b></figcaption>
</figure>

## Prerequisites

In order to successfully complete your solution, you will need to have access to and or provisioned the following:

* Access to an Azure subscription

## Getting Started

Provision the following Azure resources in your own subscription: 
1. An Azure App Service to host the frontend application (We recommend to create the App Service using VS Code: [following this link](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cvscode-aztools%2Cvscode-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli#2---create-a-web-app-in-azure))
2. An Azure App Service to host the search APIs
3. A cognitive search service to index the documents
4. A Blob storage to stage the sample documents
5. A CosmosDB with Gremlin API to store the Knowledge Graph

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
