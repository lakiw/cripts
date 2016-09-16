from tastypie import authorization
from tastypie.authentication import MultiAuthentication

from cripts.comments.comment import Comment
from cripts.comments.handlers import comment_add
from cripts.core.api import CRIPTsApiKeyAuthentication, CRIPTsSessionAuthentication
from cripts.core.api import CRIPTsSerializer, CRIPTsAPIResource


class CommentResource(CRIPTsAPIResource):
    """
    Comment API Resource Class.
    """

    class Meta:
        object_class = Comment
        allowed_methods = ('post')
        resource_name = "comments"
        authentication = MultiAuthentication(CRIPTsApiKeyAuthentication(),
                                             CRIPTsSessionAuthentication())
        authorization = authorization.Authorization()
        serializer = CRIPTsSerializer()

    def get_object_list(self, request):
        """
        Use the CRIPTsAPIResource to get our objects but provide the class to get
        the objects from.

        :param request: The incoming request.
        :type request: :class:`django.http.HttpRequest`
        :returns: Resulting objects in the specified format (JSON by default).
        """
        return super(CommentResource, self).get_object_list(request, Comment)

    def obj_create(self, bundle, **kwargs):
        """
        Handles creating Comments through the API.

        :param bundle: Bundle containing the information to create the Comment.
        :type bundle: Tastypie Bundle object.
        :returns: HttpResponse.
        """

        analyst = bundle.request.user.username
        comment = bundle.data.get('comment', None)
        obj_type = bundle.data.get('object_type', None)
        obj_id = bundle.data.get('object_id', None)

        content = {'return_code': 1,
                   'type': 'Comment',
                   'success': False}

        if not obj_type:
            content['message'] = 'Must provide an object type.'
            self.cripts_response(content)
        if not obj_id:
            content['message'] = 'Must provide an object id.'
            self.cripts_response(content)
        if not comment:
            content['message'] = 'Must provide a comment.'
            self.cripts_response(content)

        data = {'comment': comment,
                'object_type': obj_type,
                'object_id': obj_id,
                'url_key': obj_id}

        retVal = comment_add(data, obj_type, obj_id, '', {}, analyst)

        if "Comment added successfully!" in retVal.content:
            content['success'] = True
            content['return_code'] = 0
            content['message'] = 'Comment added successfully!'

        self.cripts_response(content)